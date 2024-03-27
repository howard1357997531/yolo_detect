from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import VideoOutput, VideoOutputPrivate
from auth_user.models import Profile
from pathlib import Path
import zipfile
import os
from datetime import timedelta
BASE_DIR = Path(__file__).resolve().parent.parent
# album_video
def album_video(request):
    if request.user.is_superuser:
        if Profile.objects.filter(user=request.user).first().album_date_sort:
            videos = VideoOutput.objects.all().order_by('id')
        else:
            videos = VideoOutput.objects.all().order_by('-id')
    elif request.user.is_authenticated:
        if Profile.objects.filter(user=request.user).first().album_date_sort:
            videos = VideoOutputPrivate.objects.filter(user=request.user).order_by('id')
        else:
            videos = VideoOutputPrivate.objects.filter(user=request.user).order_by('-id')
    else:
        videos = VideoOutput.objects.all().order_by('-id')

    paginator = Paginator(videos, 14)
    page = request.GET.get('page')

    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    
    # 雖然在django設定台灣時間，但這邊created_at輸出的時間還是美國時間，要使用 timedelta(hours=8, minutes=12) 做調整
    # 不然在半夜輸出的影片，在這邊時間是顯示昨天(減8小時12分鐘)
    if request.user.is_authenticated:
        if Profile.objects.filter(user=request.user).first().album_date_sort:
            date_list = sorted(list(set([(video.created_at + timedelta(hours=8, minutes=12)).strftime('%Y / %m / %d') for video in videos])))
            date_list_id = sorted(list(set([(video.created_at + timedelta(hours=8, minutes=12)).strftime('%Y%m%d') for video in videos])))
            date_zip_name = sorted(list(set(['zip/videos_' + (video.created_at + timedelta(hours=8, minutes=12)).strftime('%Y_%m_%d') + '.zip' for video in videos])))
        else:
            date_list = sorted(list(set([(video.created_at + timedelta(hours=8, minutes=12)).strftime('%Y / %m / %d') for video in videos])), reverse=True)
            date_list_id = sorted(list(set([(video.created_at + timedelta(hours=8, minutes=12)).strftime('%Y%m%d') for video in videos])), reverse=True)
            date_zip_name = sorted(list(set(['zip/videos_' + (video.created_at + timedelta(hours=8, minutes=12)).strftime('%Y_%m_%d') + '.zip' for video in videos])), reverse=True)
    else:
        date_list = sorted(list(set([(video.created_at + timedelta(hours=8, minutes=12)).strftime('%Y / %m / %d') for video in videos])), reverse=True)
        date_list_id = sorted(list(set([(video.created_at + timedelta(hours=8, minutes=12)).strftime('%Y%m%d') for video in videos])), reverse=True)
        date_zip_name = sorted(list(set(['zip/videos_' + (video.created_at + timedelta(hours=8, minutes=12)).strftime('%Y_%m_%d') + '.zip' for video in videos])), reverse=True)

    date_zip = zip(date_list, date_list_id, date_zip_name)
    context = {'videos': videos, 'date_zip': date_zip}
    return render(request, 'album_video.html', context)

def album_video_delete_ajax(request):
    if request.method == 'POST':
        video_id = request.POST.get('album_video_id')

        if request.user.is_superuser or request.user.is_anonymous:
            VideoOutput.objects.get(id=video_id).delete()
        else:
            VideoOutputPrivate.objects.get(id=video_id).delete()
        return JsonResponse({'ok': 'success'})

def album_video_delete_all_ajax(request):
    if request.method =='POST':
        date = request.POST.get('album_video_date')
        video_date = date.split('/')
        if request.user.is_superuser or request.user.is_anonymous:
            video_all = VideoOutput.objects.filter(created_at__year=int(video_date[0]), created_at__month=int(video_date[1]), 
                                         created_at__day=int(video_date[2]))
            for video in video_all:
                VideoOutput.objects.get(id=video.id).delete()
        else:
            video_all = VideoOutputPrivate.objects.filter(user=request.user, created_at__year=int(video_date[0]),
                                                          created_at__month=int(video_date[1]), created_at__day=int(video_date[2]))
            for video in video_all:
                VideoOutputPrivate.objects.get(id=video.id).delete()
        return JsonResponse({'ok': 'success'})
    
def album_video_download_all_ajax(request):
    if request.method == 'POST':
        date = request.POST.get('album_video_date')
        video_date = date.split('/')
        if request.user.is_superuser or request.user.is_anonymous:
            video_all = VideoOutput.objects.filter(created_at__year=int(video_date[0]), created_at__month=int(video_date[1]), 
                                            created_at__day=int(video_date[2]))
        else:
            video_all = VideoOutputPrivate.objects.filter(user=request.user, created_at__year=int(video_date[0]), 
                                                          created_at__month=int(video_date[1]), created_at__day=int(video_date[2]))
            
        video_url = [video.name for video in video_all]
        z = 'videos_' + '_'.join(date.split(' / ')) + '.zip'
        zip_dir = os.path.join(BASE_DIR, 'static/zip', z)
        with zipfile.ZipFile(zip_dir, mode='w') as zf:
            for url in video_url:
                if request.user.is_superuser or not request.user.is_authenticated:
                    f = os.path.join('static/media/video_output', url)
                else:
                    f = os.path.join('static/media/video_output', request.user.username, url)
                    
                zf.write(f, compress_type=zipfile.ZIP_DEFLATED)
        return JsonResponse({'ok': 'success'})

def album_video_search(request, date):
    if request.user.is_superuser or request.user.is_anonymous:
        videos = VideoOutput.objects.filter(created_at__year=int(date[:4]), created_at__month=int(date[4:6]),
                                      created_at__day=int(date[6:8])).order_by('-id')
    else:
        videos = VideoOutputPrivate.objects.filter(user=request.user, created_at__year=int(date[:4]),
                        created_at__month=int(date[4:6]), created_at__day=int(date[6:8])).order_by('-id')

    paginator = Paginator(videos, 14)
    page = request.GET.get('page')

    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        if profile.album_date_sort:
            date_list = sorted(list(set([(video.created_at + timedelta(hours=8, minutes=12)).strftime('%Y / %m / %d') for video in videos])))
            date_list_id = sorted(list(set([(video.created_at + timedelta(hours=8, minutes=12)).strftime('%Y%m%d') for video in videos])))
            date_zip_name = sorted(list(set(['zip/videos_' + (video.created_at + timedelta(hours=8, minutes=12)).strftime('%Y_%m_%d') + '.zip' for video in videos])))
        else:
            date_list = sorted(list(set([(video.created_at + timedelta(hours=8, minutes=12)).strftime('%Y / %m / %d') for video in videos])), reverse=True)
            date_list_id = sorted(list(set([(video.created_at + timedelta(hours=8, minutes=12)).strftime('%Y%m%d') for video in videos])), reverse=True)
            date_zip_name = sorted(list(set(['zip/videos_' + (video.created_at + timedelta(hours=8, minutes=12)).strftime('%Y_%m_%d') + '.zip' for video in videos])), reverse=True)
    else:
        date_list = sorted(list(set([(video.created_at + timedelta(hours=8, minutes=12)).strftime('%Y / %m / %d') for video in videos])), reverse=True)
        date_list_id = sorted(list(set([(video.created_at + timedelta(hours=8, minutes=12)).strftime('%Y%m%d') for video in videos])), reverse=True)
        date_zip_name = sorted(list(set(['zip/videos_' + (video.created_at + timedelta(hours=8, minutes=12)).strftime('%Y_%m_%d') + '.zip' for video in videos])), reverse=True)
    date_zip = zip(date_list, date_list_id, date_zip_name)
    context = {'videos': videos, 'date_zip': date_zip}
    return render(request, 'album_video_search.html', context)

def album_video_search_ajax(request):
    date = request.GET.get('dateInfo')
    date_has_photo = VideoOutput.objects.filter(created_at__year=int(date[:4]), created_at__month=int(date[4:6]),
                                          created_at__day=int(date[6:8])).exists()
    status = 'success' if date_has_photo else 'error'
    return JsonResponse({'ok': status})
