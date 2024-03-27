from django.urls import path
from . import views

app_name = 'auth_user'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register_ajax', views.register_ajax, name='register_ajax'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('settings_darkmode_ajax', views.settings_darkmode_ajax, name='settings_darkmode_ajax'),
    path('settings_album_date_sort_ajax', views.settings_album_date_sort_ajax, name='settings_album_date_sort_ajax'),
    path('alert_ajax', views.alert_ajax, name='alert_ajax'),
    path('alert_show_all/', views.alert_show_all, name='alert_show_all'),
    path('alert_check_date_quantity_ajax', views.alert_check_date_quantity_ajax, name='alert_check_date_quantity_ajax'),
    # path('alert_pure_quantity_ajax', views.alert_pure_quantity_ajax, name='alert_pure_quantity_ajax'),
    path('alert_pure_quantity_private_ajax', views.alert_pure_quantity_private_ajax, name='alert_pure_quantity_private_ajax'),
    path('analyse/', views.analyse, name='analyse'),
]