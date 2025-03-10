
from django.urls import path
from . import views

urlpatterns = [
    path('register_user/',views.register_user,name="register_user"),
    path('update_user_profile/',views.update_user_profile, name='update_user_profile'),
    path('get_username/',views.get_username,name='get_username'),
    
    path('create_blog/',views.create_blog, name='create_blog'),
    path('list_blog/',views.list_blog , name='list_blog'),
    path('get_blogs/<slug:slug>', views.get_blogs , name='get_blogs'),
    path('update_blog/<int:pk>/',views.update_blog , name='update_blog'),
    path('delete_blog/<int:pk>/',views.delete_blog, name="delete_blog"),
    path ('get_user_info/<str:username>',views.get_user_info, name='get_user_info'),
    
    
]

