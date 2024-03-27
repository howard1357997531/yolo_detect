from django.urls import path
from image import views

app_name = 'image'

urlpatterns = [
    path('photo/', views.photo, name='photo'),
    path('photo_delete_ajax', views.photo_delete_ajax, name='photo_delete_ajax'),
    path('photo_delete_all_ajax', views.photo_delete_all_ajax, name='photo_delete_all_ajax'),
    path('photo_download_all_ajax', views.photo_download_all_ajax, name='photo_download_all_ajax'),
    path('photo/<str:date>/', views.photo_search, name='photo_search'),
    path('photo_search_ajax', views.photo_search_ajax, name='photo_search_ajax'),
    path('image_multiple_folder/', views.image_multiple_folder, name='image_multiple_folder'),
    path('image_multiple_folder_delete_ajax', views.image_multiple_folder_delete_ajax, name='image_multiple_folder_delete_ajax'),
    path('image_multiple_folder_download_all_ajax', views.image_multiple_folder_download_all_ajax, name='image_multiple_folder_download_all_ajax'),
    path('image_multiple_folder_delete_all_ajax', views.image_multiple_folder_delete_all_ajax, name='image_multiple_folder_delete_all_ajax'),
    path('image_multiple_folder_delete_all_for_day_ajax', views.image_multiple_folder_delete_all_for_day_ajax, name='image_multiple_folder_delete_all_for_day_ajax'),
    path('image_multiple_folder/<str:date>/', views.image_multiple_folder_search, name='image_multiple_folder_search'),
    path('image_multiple_folder_search_ajax', views.image_multiple_folder_search_ajax, name='image_multiple_folder_search_ajax'),
]