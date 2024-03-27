from django.urls import path
from video import views

app_name = 'video'

urlpatterns = [
    path('album_video/', views.album_video, name='album_video'),
    path('album_video_delete_ajax', views.album_video_delete_ajax, name='album_video_delete_ajax'),
    path('album_video_delete_all_ajax', views.album_video_delete_all_ajax, name='album_video_delete_all_ajax'),
    path('album_video_download_all_ajax', views.album_video_download_all_ajax, name='album_video_download_all_ajax'),
    path('album_video/<str:date>/', views.album_video_search, name='album_video_search'),
    path('album_video_search_ajax', views.album_video_search_ajax, name='album_video_search_ajax'),
]