from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import (Image, ImagePrivate, ImageMultipleFolder, ImageMultipleFolderPrivate,
                     AlertImage, AlertImageNormalUser, AlertImageSuperUser,
                     AlertImageMultipleFolder, AlertImageMultipleFolderPrivate)
from auth_user.models import Profile, Alert, AlertPrivate
from pathlib import Path
import zipfile
import json
import os
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# photo
def photo(request):
    if request.user.is_superuser:
        if Profile.objects.filter(user=request.user).first().album_date_sort:
            photos = Image.objects.all().order_by('id')
        else:
            photos = Image.objects.all().order_by('-id')
    elif request.user.is_authenticated:
        if Profile.objects.filter(user=request.user).first().album_date_sort:
            photos = ImagePrivate.objects.filter(user=request.user).order_by('id')
        else:
            photos = ImagePrivate.objects.filter(user=request.user).order_by('-id')
    else:
        photos = Image.objects.all().order_by('-id')

    paginator = Paginator(photos, 30)
    page = request.GET.get('page')

    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        if Profile.objects.filter(user=request.user).first().album_date_sort:
            # 把重複日期消除，在排序(set為無序)
            date_list = sorted(list(set([(photo.created_at + timedelta(hours=8, minutes=12)).strftime('%Y / %m / %d') for photo in photos])))
            date_list_id = sorted(list(set([(photo.created_at + timedelta(hours=8, minutes=12)).strftime('%Y%m%d') for photo in photos])))
            date_zip_name = sorted(list(set(['zip/images_' + (photo.created_at + timedelta(hours=8, minutes=12)).strftime('%Y_%m_%d') + '.zip' for photo in photos])))
        else:
            date_list = sorted(list(set([(photo.created_at + timedelta(hours=8, minutes=12)).strftime('%Y / %m / %d') for photo in photos])), reverse=True)
            date_list_id = sorted(list(set([(photo.created_at + timedelta(hours=8, minutes=12)).strftime('%Y%m%d') for photo in photos])), reverse=True)
            date_zip_name = sorted(list(set(['zip/images_' + (photo.created_at + timedelta(hours=8, minutes=12)).strftime('%Y_%m_%d') + '.zip' for photo in photos])), reverse=True)
    else:
        date_list = sorted(list(set([(photo.created_at + timedelta(hours=8, minutes=12)).strftime('%Y / %m / %d') for photo in photos])), reverse=True)
        date_list_id = sorted(list(set([(photo.created_at + timedelta(hours=8, minutes=12)).strftime('%Y%m%d') for photo in photos])), reverse=True)
        date_zip_name = sorted(list(set(['zip/images_' + (photo.created_at + timedelta(hours=8, minutes=12)).strftime('%Y_%m_%d') + '.zip' for photo in photos])), reverse=True)

    date_zip = zip(date_list, date_list_id, date_zip_name)
    context = {'photos': photos, 'date_zip': date_zip}

    return render(request, 'photo.html', context)

def photo_delete_ajax(request):
    if request.method == 'POST':
        photo_id = request.POST.get('id')

        if request.user.is_superuser:
            Image.objects.get(id=photo_id).delete()
        else:
            ImagePrivate.objects.get(id=photo_id).delete()
        # print('image delete') # 順序 signals.py pre_delete -> post_delete -> 這裡(views.py)
                                # 不知為何不是    pre_delete -> 這裡(views.py) -> post_delete
        return JsonResponse({'ok': 'success'})

def photo_delete_all_ajax(request):
    if request.method =='POST':
        date = request.POST.get('photo_date')
        photo_date = date.split('/')
        if request.user.is_superuser:
            photo_all = Image.objects.filter(created_at__year=int(photo_date[0]), created_at__month=int(photo_date[1]), 
                                            created_at__day=int(photo_date[2]))
            for photo in photo_all:
                Image.objects.get(id=photo.id).delete()
        else:
            photo_all = ImagePrivate.objects.filter(user=request.user, created_at__year=int(photo_date[0]),
                                            created_at__month=int(photo_date[1]), created_at__day=int(photo_date[2]))
            for photo in photo_all:
                ImagePrivate.objects.get(id=photo.id).delete()
        return JsonResponse({'ok': 'success'})
    
def photo_download_all_ajax(request):
    if request.method == 'POST':
        date = request.POST.get('photo_date')
        photo_date = date.split('/')
        if request.user.is_superuser or not request.user.is_authenticated:
            photo_all = Image.objects.filter(created_at__year=int(photo_date[0]), created_at__month=int(photo_date[1]), 
                                            created_at__day=int(photo_date[2]))
        else:
            photo_all = ImagePrivate.objects.filter(user=request.user, created_at__year=int(photo_date[0]), 
                                                    created_at__month=int(photo_date[1]), created_at__day=int(photo_date[2]))

        image_url = [photo.name for photo in photo_all]
        # print(photo_date)
        # print(photo_all)
        # print(photo_url)
        # print(int('05')) # 5
        zip_name = 'images_' + '_'.join(date.split(' / ')) + '.zip'
        # print(z)
        # 不知道在建立zip之前先把資料夾清空會不會增加效益
        zip_dir = os.path.join(BASE_DIR, 'static/zip', zip_name)
        with zipfile.ZipFile(zip_dir, mode='w') as zf:
            for url in image_url:
                # 建立出來zip裡面的子資料夾數是由 f 來決定
                # work\a\project1\yolo_detect\static\media\image 下述會有7層資料夾
                # f = os.path.join(settings.MEDIA_ROOT, 'image', url)
                if request.user.is_superuser or not request.user.is_authenticated:
                    f = os.path.join('static/media/image', url)
                else:
                    f = os.path.join('static/media/image', request.user.username, url)

                zf.write(f, compress_type=zipfile.ZIP_DEFLATED)
        return JsonResponse({'ok': 'success'})

def photo_search(request, date):
    if request.user.is_superuser or request.user.is_anonymous:
        photos = Image.objects.filter(created_at__year=int(date[:4]), created_at__month=int(date[4:6]),
                                      created_at__day=int(date[6:8])).order_by('-id')
    else:
        photos = ImagePrivate.objects.filter(user=request.user, created_at__year=int(date[:4]),
                    created_at__month=int(date[4:6]), created_at__day=int(date[6:8])).order_by('-id')

    paginator = Paginator(photos, 14)
    page = request.GET.get('page')

    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)
    
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        if profile.album_date_sort:
            date_list = sorted(list(set([(photo.created_at + timedelta(hours=8, minutes=12)).strftime('%Y / %m / %d') for photo in photos])))
            date_list_id = sorted(list(set([(photo.created_at + timedelta(hours=8, minutes=12)).strftime('%Y%m%d') for photo in photos])))
            date_zip_name = sorted(list(set(['zip/images_' + (photo.created_at + timedelta(hours=8, minutes=12)).strftime('%Y_%m_%d') + '.zip' for photo in photos])))
        else:
            date_list = sorted(list(set([(photo.created_at + timedelta(hours=8, minutes=12)).strftime('%Y / %m / %d') for photo in photos])), reverse=True)
            date_list_id = sorted(list(set([(photo.created_at + timedelta(hours=8, minutes=12)).strftime('%Y%m%d') for photo in photos])), reverse=True)
            date_zip_name = sorted(list(set(['zip/images_' + (photo.created_at + timedelta(hours=8, minutes=12)).strftime('%Y_%m_%d') + '.zip' for photo in photos])), reverse=True)
    else:
        date_list = sorted(list(set([(photo.created_at + timedelta(hours=8, minutes=12)).strftime('%Y / %m / %d') for photo in photos])), reverse=True)
        date_list_id = sorted(list(set([(photo.created_at + timedelta(hours=8, minutes=12)).strftime('%Y%m%d') for photo in photos])), reverse=True)
        date_zip_name = sorted(list(set(['zip/images_' + (photo.created_at + timedelta(hours=8, minutes=12)).strftime('%Y_%m_%d') + '.zip' for photo in photos])), reverse=True)
    date_zip = zip(date_list, date_list_id, date_zip_name)
    context = {'photos': photos, 'date_zip': date_zip}
    return render(request, 'photo_search.html', locals())

def photo_search_ajax(request):
    date = request.GET.get('dateInfo')
    date_has_photo = Image.objects.filter(created_at__year=int(date[:4]), created_at__month=int(date[4:6]),
                                          created_at__day=int(date[6:8])).exists()
    status = 'success' if date_has_photo else 'error'
    return JsonResponse({'ok': status})

# image_multiple_folder
#photo_count = [ImageMultipleFolder.objects.filter(code=folder[0]).count() for folder in folder_code]
def image_multiple_folder(request):
    if request.user.is_superuser:
        folder_code = ImageMultipleFolder.objects.values_list('code').distinct() # ex: <QuerySet [(1,), (2,), (3,), (4,), (5,)]>
        if Profile.objects.filter(user=request.user).first().album_date_sort:
            folders = [ImageMultipleFolder.objects.filter(code=folder[0]).first() for folder in folder_code]
        else:
            folders = [ImageMultipleFolder.objects.filter(code=folder[0]).first() for folder in folder_code][::-1]
        photo_all_modal = ImageMultipleFolder.objects.all()
    elif request.user.is_authenticated:
        folder_code = ImageMultipleFolderPrivate.objects.values_list('code').distinct() # ex: <QuerySet [(1,), (2,), (3,), (4,), (5,)]>
        if Profile.objects.filter(user=request.user).first().album_date_sort:
            folders = [ImageMultipleFolderPrivate.objects.filter(code=folder[0]).first() for folder in folder_code]
        else:
            folders = [ImageMultipleFolderPrivate.objects.filter(code=folder[0]).first() for folder in folder_code][::-1]
        photo_all_modal = ImageMultipleFolderPrivate.objects.all()
    else :
        folder_code = ImageMultipleFolder.objects.values_list('code').distinct()
        folders = [ImageMultipleFolder.objects.filter(code=folder[0]).first() for folder in folder_code][::-1]
        photo_all_modal = ImageMultipleFolder.objects.all()

    paginator = Paginator(folders, 14)
    page = request.GET.get('page')

    try:
        folders = paginator.page(page)
    except PageNotAnInteger:
        folders = paginator.page(1)
    except EmptyPage:
        folders = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        if Profile.objects.filter(user=request.user).first().album_date_sort:
            date_list = sorted(list(set([(date.created_at + timedelta(hours=8, minutes=12)).strftime('%Y / %m / %d') for date in folders])))
            photo_created_at = [(date.created_at + timedelta(hours=8, minutes=12)).strftime('%Y%m%d') for date in folders]
        else:
            date_list = sorted(list(set([(date.created_at + timedelta(hours=8, minutes=12)).strftime('%Y / %m / %d') for date in folders])), reverse=True)
            photo_created_at = [(date.created_at + timedelta(hours=8, minutes=12)).strftime('%Y%m%d') for date in folders]
    else:
        date_list = sorted(list(set([(date.created_at + timedelta(hours=8, minutes=12)).strftime('%Y / %m / %d') for date in folders])), reverse=True)
        photo_created_at = [(date.created_at + timedelta(hours=8, minutes=12)).strftime('%Y%m%d') for date in folders]
    folder_code_modal = [i.code for i in folders]
    
    folder_zip = zip(folder_code_modal, photo_created_at)

    context = {'date_list': date_list, 'photo_all_modal': photo_all_modal,
               'folders': folders, 'folder_zip': folder_zip}
    return render(request, 'image_multiple_folder.html', context)

# 資料夾內單個照片刪除
def image_multiple_folder_delete_ajax(request):
    if request.method == 'POST':
        photo_id = request.POST.get('photo_id')
        if request.user.is_superuser:
            code = ImageMultipleFolder.objects.filter(id=int(photo_id)).first().code
            # 因為anony_user不能做刪除公共相簿的操作，所以要在superuser做刪除，所以要先檢查folder_code是不是superuser創建的
            if AlertImageMultipleFolderPrivate.objects.filter(user=request.user, folder_code=code, is_deleted=False).exists():
                alert = AlertImageMultipleFolderPrivate.objects.filter(user=request.user, folder_code=code, is_deleted=False).first()
            else:
                alert = AlertImageMultipleFolder.objects.filter(folder_code=code, is_deleted=False).first()
            ImageMultipleFolder.objects.get(id=int(photo_id)).delete()
        elif request.user.is_authenticated:
            code = ImageMultipleFolderPrivate.objects.filter(user=request.user, id=int(photo_id)).first().code
            alert = AlertImageMultipleFolderPrivate.objects.filter(user=request.user, folder_code=code, is_deleted=False).first()
            ImageMultipleFolderPrivate.objects.get(user=request.user, id=int(photo_id)).delete()

        if alert.total_quantity == 1:
            alert.is_deleted = True
            alert.save(update_fields=['is_deleted'])
        else:
            alert.delete_quantity += 1
            alert.save(update_fields=['delete_quantity', 'total_quantity'])
        return JsonResponse({'ok': 'success'})

def image_multiple_folder_delete_all_ajax(request):
    if request.method == 'POST':
        photo_id_array = request.POST.get('photo_id_array')
        photo_id_list = json.loads(photo_id_array) # 從字串(json)轉成串列
        
        # alert
        # 用try是因為之後想做定期刪除alert,所以在刪除時會找不到folder_code,會error
        try:
            if request.user.is_superuser:
                code = ImageMultipleFolder.objects.filter(id=int(photo_id_list[0])).first().code
                if AlertImageMultipleFolderPrivate.objects.filter(user=request.user, folder_code=code, is_deleted=False).exists():
                    alert = AlertImageMultipleFolderPrivate.objects.filter(user=request.user, folder_code=code, is_deleted=False).first()
                else:
                    alert = AlertImageMultipleFolder.objects.filter(folder_code=code, is_deleted=False).first()
            elif request.user.is_authenticated:
                code = ImageMultipleFolderPrivate.objects.filter(user=request.user, id=int(photo_id_list[0])).first().code
                alert = AlertImageMultipleFolderPrivate.objects.filter(user=request.user, folder_code=code, is_deleted=False).first()
            alert.is_deleted = True
            alert.save()
        except:
            pass    

        if request.user.is_superuser:
            for photo in photo_id_list:
                ImageMultipleFolder.objects.get(id=int(photo)).delete()
        elif request.user.is_authenticated:
            for photo in photo_id_list:
                ImageMultipleFolderPrivate.objects.get(user=request.user, id=int(photo)).delete()
        
        return JsonResponse({'ok': 'success'})
    
def image_multiple_folder_delete_all_for_day_ajax(request):
    if request.method == 'POST':
        photo_date = request.POST.get('photo_date').split(' / ')
        # alert
        try:
            alert = AlertImageMultipleFolder.objects.filter(created_at__year=int(photo_date[0]),
                    created_at__month=int(photo_date[1]), created_at__day=int(photo_date[2]))
            alert_private = AlertImageMultipleFolderPrivate.objects.filter(
                    user=request.user, created_at__year=int(photo_date[0]), 
                    created_at__month=int(photo_date[1]), created_at__day=int(photo_date[2]))
            if request.user.is_superuser:
                if alert.exists():
                    alert.update(is_deleted=True)
            if alert_private.exists():
                alert_private.update(is_deleted=True)
        except:
            pass

        if request.user.is_superuser:
            photo_all = ImageMultipleFolder.objects.filter(created_at__year=int(photo_date[0]),
                    created_at__month=int(photo_date[1]), created_at__day=int(photo_date[2]))
        elif request.user.is_authenticated:
            photo_all = ImageMultipleFolderPrivate.objects.filter(
                    user=request.user, created_at__year=int(photo_date[0]), 
                    created_at__month=int(photo_date[1]), created_at__day=int(photo_date[2]))
        
        for photo in photo_all:
            photo.delete()
        
        return JsonResponse({'ok': 'success'})

def image_multiple_folder_download_all_ajax(request):
    if request.method == 'POST':
        photo_code = request.POST.get('photo_code')
        if request.user.is_superuser or request.user.is_anonymous:
            photo_name = [photo.name for photo in ImageMultipleFolder.objects.filter(code=int(photo_code))]
        else :
            photo_name = [photo.name for photo in ImageMultipleFolderPrivate.objects.filter(user=request.user, code=int(photo_code))]
        # zip_name = 'image_multiple_folder_' + photo_code + '.zip'
        zip_name = 'image_multiple_folder.zip'
        zip_dir = os.path.join(BASE_DIR, 'static/zip', zip_name)
        with zipfile.ZipFile(zip_dir, mode='w') as zf:
            for photo in photo_name:
                if request.user.is_superuser or request.user.is_anonymous:
                    f = os.path.join('static/media/image_multiple_folder', photo_code, photo)
                else :
                    f = os.path.join('static/media/image_multiple_folder_private', request.user.username, photo_code, photo)
                zf.write(f, compress_type=zipfile.ZIP_DEFLATED)
        return JsonResponse({'ok': 'success'})

def image_multiple_folder_search(request, date):
    if request.user.is_superuser or request.user.is_anonymous:
        folder_code = ImageMultipleFolder.objects.values_list('code').distinct() # ex: <QuerySet [(1,), (2,), (3,), (4,), (5,)]>
        folders = [ImageMultipleFolder.objects.filter(code=folder[0], created_at__year=int(date[:4]), created_at__month=int(date[4:6]),
                                                      created_at__day=int(date[6:8])).first() for folder in folder_code 
                   if ImageMultipleFolder.objects.filter(code=folder[0], created_at__year=int(date[:4]), created_at__month=int(date[4:6]),
                                                      created_at__day=int(date[6:8])).first() != None][::-1]
        photo_all = ImageMultipleFolder.objects.all()
        photo_count = [ImageMultipleFolder.objects.filter(code=folder[0]).count() for folder in folder_code]
    else :
        folder_code = ImageMultipleFolderPrivate.objects.filter(user=request.user).values_list('code').distinct()
        folders = [ImageMultipleFolderPrivate.objects.filter(user=request.user, code=folder[0], created_at__year=int(date[:4]),
                   created_at__month=int(date[4:6]), created_at__day=int(date[6:8])).first() for folder in folder_code
                   if ImageMultipleFolderPrivate.objects.filter(user=request.user, code=folder[0], created_at__year=int(date[:4]),
                   created_at__month=int(date[4:6]), created_at__day=int(date[6:8])).first() != None][::-1]
        photo_all = ImageMultipleFolderPrivate.objects.filter(user=request.user)
        photo_count = [ImageMultipleFolderPrivate.objects.filter(user=request.user, code=folder[0]).count() for folder in folder_code]

    paginator = Paginator(folders, 14)
    page = request.GET.get('page')

    try:
        folders = paginator.page(page)
    except PageNotAnInteger:
        folders = paginator.page(1)
    except EmptyPage:
        folders = paginator.page(paginator.num_pages)

    date_list = sorted(list(set([(date.created_at + timedelta(hours=8, minutes=12)).strftime('%Y / %m / %d') for date in list(folders)])), reverse=True)
    folder_modal_code = [i.code for i in folders]
    photo_created_at = [(date.created_at + timedelta(hours=8, minutes=12)).strftime('%Y%m%d') for date in folders[::-1]]
    folder_zip = zip(folder_modal_code, photo_count, photo_created_at)

    context = {'date_list': date_list, 'photo_all': photo_all,
               'folders': folders, 'folder_zip': folder_zip}
    return render(request, 'image_multiple_folder_search.html', context)

def image_multiple_folder_search_ajax(request):
    date = request.GET.get('dateInfo')
    if request.user.is_superuser or request.user.is_anonymous:
        date_has_photo = ImageMultipleFolder.objects.filter(created_at__year=int(date[:4]), created_at__month=int(date[4:6]),
                                            created_at__day=int(date[6:8])).exists()
    else :
        date_has_photo = ImageMultipleFolderPrivate.objects.filter(user=request.user, created_at__year=int(date[:4]),
                                            created_at__month=int(date[4:6]), created_at__day=int(date[6:8])).exists()
    status = 'success' if date_has_photo else 'error'
    return JsonResponse({'ok': status})
