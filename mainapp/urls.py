from django.urls import path
from mainapp import views, camera_split

app_name = 'mainapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('web_camera/', views.web_camera, name='web_camera'),
    path('web_camera_video_feed/', views.web_camera_video_feed, name='web_camera_video_feed'),
    path('intel_camera/', views.intel_camera, name='intel_camera'),
    path('intel_camera_video_feed/', views.intel_camera_video_feed, name='intel_camera_video_feed'),
    path('check_intel_camera_isopen/', views.check_intel_camera_isopen, name='check_intel_camera_isopen'),
    path('camera_split/', views.camera_split, name="camera_split"),
    path('image/', views.image, name='image'),
    path('image_detect', views.image_detect, name='image_detect'),
    path('image_multiple/', views.image_multiple, name='image_multiple'),
    path('image_multiple_ajax', views.image_multiple_ajax, name='image_multiple_ajax'),
    path('image_multiple_folder_ajax', views.image_multiple_folder_ajax, name='image_multiple_folder_ajax'),
    path('video/', views.video, name='video'),
    path('get_video', views.get_video, name='get_video'),
    path('video_video_feed/', views.video_video_feed, name='video_video_feed'),
    path('video_merge_ajax', views.video_merge_ajax, name='video_merge_ajax'),

    # camera_split
    path('camera_split_setting/', views.camera_split_setting, name='camera_split_setting'),
    path('camera_split_setting_ajax', views.camera_split_setting_ajax, name='camera_split_setting_ajax'),
    path('web_camera_video_feed_split/<str:mode>/', camera_split.web_camera_video_feed_split, name='web_camera_video_feed_split'),
    path('intel_camera_video_feed_split/<str:mode>/', camera_split.intel_camera_video_feed_split, name='intel_camera_video_feed_split'),
    path('all_camera_video_feed/<str:camera_name>/', camera_split.all_camera_video_feed, name='all_camera_video_feed'),
]