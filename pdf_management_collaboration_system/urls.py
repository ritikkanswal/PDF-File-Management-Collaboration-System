from django.contrib import admin
from django.urls import path
from app import views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.HomePage,name='home'),
    path('signup/',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('home/',views.HomePage,name='home'),
    path('logout/',views.LogoutPage,name='logout'),
    path('upload/', views.HomePage, name='home'),
    path('users/', views.user_list, name='user_list'),

    path('file/<uuid:file_uuid>/', views.file, name='file'),
    path('add_comment/', views.add_comment, name='add_comment'),
    # path('search/', views.SearchView.as_view(), name='search'), 
    path('search/', views.search_files, name='search'),
    path('search/', views.search_users, name='search_users'),
    path('api/upload/', views.upload, name='upload'),
    path('api/files/', views.files, name='files'),
    path('api/share/', views.share, name='share'),

]