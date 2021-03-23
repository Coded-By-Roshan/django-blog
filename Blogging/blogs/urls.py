from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
     path('',views.home , name='home' ),
     path('detail/<int:pk>',views.detail , name='detail' ),
     path('addBlog',views.add_view , name='addBlog' ),
     path('login', views.login_view, name='login'),
     path('login_page', views.login_page, name='login_page'),
     path('logout', views.logout_view, name='logout'),
     path('signUp', views.signUp_view, name='signUp'),
     path('search', views.search, name='search'),
     path('contact', views.contact, name='contact'),
     path('comment',views.comments , name='comment' ),
     path('managecontact', views.managecontact, name='managecontact'),
     path('subscribe', views.subscribe, name='subscribe'),
     path('edit/<int:id>',views.edit , name='edit' ),
    path('delete',views.delete , name='delete' ),
     
]