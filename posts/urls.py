from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home , name='home' ),
    path('blogs',views.blog , name='blog' ),
    # path('register',views.register , name='register' ),
    path('contact',views.contact , name='contact' ),
    path('addpost',views.add , name='add' ),
    path('login', views.logging , name='login' ),
    path('logout' ,views.logout , name='logout' ),
    path('managecontact' ,views.managecontact , name='managecontact' ),
    path('detail/<int:pk>',views.detail , name='detail' ),
    path('comment',views.comments , name='comment' ),
    path('search',views.search , name='search' ),
    path('edit/<int:id>',views.edit , name='edit' ),
    path('delete',views.delete , name='delete' ),
    path('subscribe',views.subscribe , name='subscribe' ),
    path('password-reset/',auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'), 
]