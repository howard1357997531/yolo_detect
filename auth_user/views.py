from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import auth, messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Max
from .forms import RegisterForm, ProfileForm
from image.models import (Image, ImagePrivate, ImageMultipleFolder, ImageMultipleFolderPrivate,
                          AlertImage, AlertImageNormalUser, AlertImageSuperUser,
                          AlertImageMultipleFolder, AlertImageMultipleFolderPrivate)
from video.models import VideoOutput, VideoOutputPrivate, AlertVideo, AlertVideoNormalUser, AlertVideoSuperUser
from .models import Profile, Alert, AlertPrivate, AlertPureQuantity, AlertPureQuantityPrivate


def is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'

def register(request):
    if request.user.is_authenticated:
        return redirect('mainapp:home')
    else:
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    if user.is_active:
                        auth.login(request, user)
                        messages.success(request, '建立帳號成功')
                        return redirect('mainapp:web_camera')

    return render(request, 'register.html', locals())

def register_ajax(request):
    form = RegisterForm()
    if request.method == 'POST':
        #print(request.POST)
        form = RegisterForm(request.POST)
        #print(form.is_valid())
        #print(form.errors)
        #print(dict(form.errors))
        #print(dict(form.errors)['username'])
        #print(type(str(dict(form.errors)['username'])))
        if form.is_valid():
            # form.save()
            messages.success(request, '建立帳號成功')
            return JsonResponse({'ok': 'success', 's': dict(form.errors)['username']})
    return JsonResponse({'ok': 'success'})

def login(request):
    if request.user.is_authenticated:
        return redirect('mainapp:home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, '登入成功')
                    return redirect('mainapp:web_camera')
            else:
                messages.error(request, '無效的帳號或密碼')
    return render(request, 'login.html', locals())

def logout(request):
    auth.logout(request)
    messages.success(request, '已登出')
    return redirect('auth_user:login')


@login_required()
def profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,
                             instance=request.user.profile)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not Profile.objects.filter(email=email).exclude(user=request.user).exists():
                form.save()
                messages.success(request, '修改成功')
                return redirect('mainapp:web_camera')
            else:
                messages.error(request, '電子郵件已被使用')
    else:
        form = ProfileForm(instance=request.user.profile)
    context = {'profile': profile, 'form': form}
    return render(request, 'profile.html', context)

@login_required
def settings(request):
    return render(request, 'settings.html', locals())

@login_required
def settings_darkmode_ajax(request):
    if request.method == 'POST':
        darkmode_checked = request.POST.get('darkmode_check')
        darkmode_checked = True if darkmode_checked == 'true' else False
        profile = Profile.objects.get(user=request.user)
        profile.darkmode = darkmode_checked
        profile.save()
    return JsonResponse({'ok': 'success'})

@login_required
def settings_album_date_sort_ajax(request):
    if request.method == 'POST':
        album_date_sort_checked = request.POST.get('album_date_sort_check')
        album_date_sort_checked = True if album_date_sort_checked == 'true' else False
        print(album_date_sort_checked)
        profile = Profile.objects.get(user=request.user)
        profile.album_date_sort = album_date_sort_checked
        profile.save()

        return JsonResponse({'ok': 'success'})

def alert_ajax(request):
    if request.method == 'POST' and is_ajax(request):        
        if request.user.is_superuser:
            # 使用.update() 也不會更新 modified_at
            AlertImageSuperUser.objects.filter(user=request.user, is_checked=False).update(is_checked=True)
            AlertVideoSuperUser.objects.filter(user=request.user, is_checked=False).update(is_checked=True)
        elif request.user.is_authenticated:
            AlertImageNormalUser.objects.filter(user=request.user, is_checked=False).update(is_checked=True)
            AlertVideoNormalUser.objects.filter(user=request.user, is_checked=False).update(is_checked=True)
        else:
            AlertImage.objects.filter(is_checked=False).update(is_checked=True)

        if request.user.is_authenticated:
            AlertPrivate.objects.filter(user=request.user, is_checked=False).update(is_checked=True)
            AlertImageMultipleFolderPrivate.objects.filter(user=request.user, is_checked=False).update(is_checked=True)
            AlertPureQuantityPrivate.objects.filter(user=request.user, is_checked=False).update(is_checked=True)
        else:
            Alert.objects.filter(is_checked=False).update(is_checked=True)
            AlertImageMultipleFolder.objects.filter(is_checked=False).update(is_checked=True)
            AlertPureQuantity.objects.filter(is_checked=False).update(is_checked=True)

        # 刪除40則之後的alert
        if request.user.is_authenticated:
            alerts = AlertPrivate.objects.filter(user=request.user).order_by('-id')
        else:
            alerts = Alert.objects.all().order_by('-id')
        if alerts.count() > 40:
            for alert in alerts[40:]:
                alert.delete()
        
        return JsonResponse({'ok': 'success'})
    
def alert_show_all(request):
    if request.user.is_authenticated:
        alerts = AlertPrivate.objects.filter(user=request.user).order_by('-id')
        folders = AlertImageMultipleFolderPrivate.objects.filter(user=request.user).order_by('-id')
        pure_quantity = AlertPureQuantityPrivate.objects.filter(user=request.user).order_by('-id')
    else:
        alerts = Alert.objects.all().order_by('-id')
        folders = AlertImageMultipleFolder.objects.all().order_by('-id')
        pure_quantity = AlertPureQuantity.objects.all().order_by('-id')

    if request.user.is_superuser:
        images = AlertImageSuperUser.objects.filter(user=request.user).order_by('-id')
        videos = AlertVideoSuperUser.objects.filter(user=request.user).order_by('-id')
    elif request.user.is_authenticated:
        images = AlertImageNormalUser.objects.filter(user=request.user).order_by('-id')
        videos = AlertVideoNormalUser.objects.filter(user=request.user).order_by('-id')
    else:
        images = AlertImage.objects.all().order_by('-id')
        videos = AlertVideo.objects.all().order_by('-id')

    paginator = Paginator(alerts, 8)
    page = request.GET.get('page')

    try:
        alerts = paginator.page(page)
    except PageNotAnInteger:
        alerts = paginator.page(1)
    except EmptyPage:
        alerts = paginator.page(paginator.num_pages)
    
    context = {'alerts': alerts, 'images': images, 'videos': videos, 'folders': folders,
               'pure_quantity': pure_quantity}
    return render(request, 'alert_show_all.html', context)

def alert_check_date_quantity_ajax(request):
    if request.method == 'GET' and is_ajax(request):
        item = request.GET.get('item')
        item_id = request.GET.get('item_id') 
        date = request.GET.get('date')

        if request.user.is_superuser or request.user.is_anonymous:
            if item == 'folder':
                alert = ImageMultipleFolder.objects.filter(created_at__year=int(date[:4]), created_at__month=int(date[4:6]),
                                                created_at__day=int(date[6:8]))
            elif item == 'image':
                alert = Image.objects.filter(created_at__year=int(date[:4]), created_at__month=int(date[4:6]),
                                                created_at__day=int(date[6:8]))
            elif item == 'video':
                alert = VideoOutput.objects.filter(created_at__year=int(date[:4]), created_at__month=int(date[4:6]),
                                                created_at__day=int(date[6:8]))
        else:
            if item == 'folder':
                alert = ImageMultipleFolderPrivate.objects.filter(user=request.user, created_at__year=int(date[:4]),
                                                created_at__month=int(date[4:6]), created_at__day=int(date[6:8]))
            elif item == 'image':
                alert = ImagePrivate.objects.filter(user=request.user, created_at__year=int(date[:4]),
                                                created_at__month=int(date[4:6]),created_at__day=int(date[6:8]))
            elif item == 'video':
                alert = VideoOutputPrivate.objects.filter(user=request.user, created_at__year=int(date[:4]),
                                                created_at__month=int(date[4:6]), created_at__day=int(date[6:8]))
        if item == 'folder':
            alert_id_list = list(set([a.code for a in alert]))
            alert_id_list.sort()
        else:
            alert_id_list = [a.id for a in alert]
        alert_index = alert_id_list[::-1].index(int(item_id)) + 1
        return JsonResponse({'ok': 'success', 'alert_index': alert_index})

# @login_required
# def alert_pure_quantity_ajax(request):
#     if request.method == 'POST' and is_ajax(request):
#         name = request.POST.get('name')

#         if AlertPureQuantityPrivate.objects.filter(user=request.user).exists():
#             max_code = AlertPureQuantityPrivate.objects.filter(user=request.user).aggregate(Max('code')).get('code__max')
#             max_code = max_code if AlertPureQuantityPrivate.objects.filter(user=request.user, is_checked=False).exists() else max_code + 1
#             AlertPureQuantityPrivate.objects.create(user=request.user, name=name, code=max_code)
#         else:
#             max_code = 1
#             AlertPureQuantityPrivate.objects.create(user=request.user, name=name)

#         alert, created = AlertPrivate.objects.get_or_create(user=request.user ,is_checked=False)
#         alert.total_quantity += 1
#         alert.alert_pure_code = max_code
#         if name == 'profile_setting':
#             alert.alert_pure_profile_setting_quantity += 1
#         elif name == 'password_change':
#             alert.alert_pure_password_change_quantity += 1

#         last_one_item = alert.last_one_item
#         if last_one_item == 'none':
#             alert.last_one_item == name
#         else:
#             if last_one_item != name:
#                 alert.last_one_item = name
#                 alert.last_two_item = last_one_item
#         alert.save()

#         return JsonResponse({'ok': 'success'})
    
@login_required
def alert_pure_quantity_private_ajax(request):
    if request.method == 'POST' and is_ajax(request):
        name = request.POST.get('name')

        if AlertPureQuantityPrivate.objects.filter(user=request.user).exists():
            max_code = AlertPureQuantityPrivate.objects.filter(user=request.user).aggregate(Max('code')).get('code__max')
            max_code = max_code if AlertPureQuantityPrivate.objects.filter(user=request.user, is_checked=False).exists() else max_code + 1
            AlertPureQuantityPrivate.objects.create(user=request.user, name=name, code=max_code)
        else:
            max_code = 1
            AlertPureQuantityPrivate.objects.create(user=request.user, name=name)

        alert, created = AlertPrivate.objects.get_or_create(user=request.user ,is_checked=False)
        alert.total_quantity += 1
        alert.alert_pure_code = max_code
        if name == 'profile_setting':
            alert.alert_pure_profile_setting_quantity += 1
        elif name == 'password_change':
            alert.alert_pure_password_change_quantity += 1

        last_one_item = alert.last_one_item
        print(last_one_item)
        if last_one_item == 'none':
            alert.last_one_item = name
        else:
            if last_one_item != name:
                alert.last_one_item = name
                alert.last_two_item = last_one_item
        alert.save()

        return JsonResponse({'ok': 'success'})

def analyse(request):
    if request.user.is_superuser or not request.user.is_authenticated:
        image_all = Image.objects.all()
        im = [image.created_at.strftime('%m / %d') for image in image_all]
        im = sorted(list(set(im)))
        print(im)
        im_count = []
        im_pm_count = []
        for i in im :
            c = Image.objects.filter(created_at__month=int(i[:2]), created_at__day=int(i[-2:])).count()
            pm = Image.objects.filter(created_at__month=int(i[:2]), created_at__day=int(i[-2:]),
                                    created_at__hour__gt=12).count()
            im_count.append(c)
            im_pm_count.append(pm)

        image = Image.objects.all().count()
        video = VideoOutput.objects.all().count()
        ratio_list = [image, video]
    else:
        image_all = ImagePrivate.objects.all()
        im = [image.created_at.strftime('%m / %d') for image in image_all]
        im = sorted(list(set(im)))
        print(im)
        im_count = []
        im_pm_count = []
        for i in im :
            c = ImagePrivate.objects.filter(created_at__month=int(i[:2]), created_at__day=int(i[-2:])).count()
            pm = ImagePrivate.objects.filter(created_at__month=int(i[:2]), created_at__day=int(i[-2:]),
                                    created_at__hour__gt=12).count()
            im_count.append(c)
            im_pm_count.append(pm)

        image = ImagePrivate.objects.all().count()
        video = VideoOutputPrivate.objects.all().count()
        ratio_list = [image, video]
    return render(request, 'analyse.html', locals())