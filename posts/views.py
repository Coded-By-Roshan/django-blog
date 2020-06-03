from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import BlogForm, Userregister
from .models import Blog, Comment, Subscribe
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail  
from django.core.paginator import Paginator
from django.views.generic import ListView




def home(request):
    if request.method == 'POST':
        form = Userregister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            form.save()
            messages.success(request, f"You have successfully registered as {username} ")
    else:
        form = Userregister()
    params = {'form':form ,'title':'Home'}
    return render(request, 'home.html', params)


@login_required(login_url='/home')
def logout(request):
    auth_logout(request)
    return redirect('home')

def logging(request):
    if request.method == 'POST':
        email = request.POST['login-email']
        password = request.POST['login-pswd']
        user = authenticate(username=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(
                request, 'you have successfully login into your account')
        else:
            
            messages.error(request, 'user name and password didnot match. try again ')
    
    return redirect('home')



def blog(request):
    blogs = Blog.objects.all().order_by('-timestamp')
    blogpage = Paginator(blogs, 5)
    page_number = request.GET.get('page')
    page_obj = blogpage.get_page(page_number)
    params = {'blogs':blogs, 'page_obj':page_obj, 'title':'Blog'}
    return render(request, 'blogs.html', params)


def contact(request):
    params = {'title':'Contact'}
    return render(request, 'contact.html')

def subscribe(request):
    if request.method == 'POST':
        emails = request.POST['subscribe']
        subs = Subscribe(email = emails)
        subs.save()
        messages.success(request, 'You have subscribed to our blog. Now you will get latest information about it.')
    return redirect(home)

def detail(request, pk):
    blogpost = Blog.objects.filter(pk=pk)
    blogs = Blog.objects.filter(pk=pk).first()
    blogs.views = blogs.views + 1
    blogs.save()
    comments = Comment.objects.filter(post=blogs).order_by('-timestamp')
    contex = {'title': 'fullpost', 'blogs': blogpost,
              'comments': comments}
    return render(request, 'blogdetail.html', contex)


@login_required(login_url='/home')
def add(request):
    if request.method == 'POST':
        form = BlogForm(request.POST , request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            image = form.cleaned_data['image']
            user =  request.user
            blog = Blog(title=title, description=description, image=image, user=user )
            blog.save()
            messages.success(request, "You have Successfully Posted a Post")
        
    else:
        form = BlogForm()
    params = {'form':form}
    return render(request, 'addblog.html', params)

def managecontact(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        contactmessage = request.POST.get('contactmessage')
        send_mail('Blog message', 
        contactmessage,
        email,
        ['kingspider224@gmail.com'],
        fail_silently=False
        )
        messages.success(request, 'Your Email Has Successfully sent to your admin')
    return redirect(contact)

def comments(request):
    if request.method == 'POST':
        user = request.user
        post = int(request.POST['post'])
        cmt = request.POST['cmt']
        blog = Blog.objects.get(id=post)
        blogcmt = Comment(user=user, post=blog, comment=cmt)
        blogcmt.save()
        messages.success(request, "You Have Successfully Posted a Comment")
    return redirect(f'detail/{post}')


def search(request):
    query = request.POST['query']
    if len(query) > 15:
        return render(request, 'error.html')
    if len(query) <= 0:
        messages.error(request, "Please pass correct keyword to search")
        return redirect(blog)
    searchblog = Blog.objects.filter(title__icontains=query)
    if searchblog.count() == 0:
        return HttpResponse("<h1>NO RESULT FOUND</h1>")
    params = {'searchblog':searchblog}
    return render(request, 'search.html', params)

def edit(request, id):
    edit_blog = Blog.objects.get(pk=id)
    form = BlogForm(request.POST, request.FILES, instance= edit_blog)
    if form.is_valid():
        form.save()
    else:
        form = BlogForm(instance=edit_blog)
    params = {'form':form}
    return render(request, 'editblog.html', params)


def delete(request):
    if request.method == 'POST':
        delete_item_id = request.POST['delete-id']
        delete_item = Blog.objects.filter(pk = delete_item_id)
        delete_item.delete()
        
    return redirect(blog)