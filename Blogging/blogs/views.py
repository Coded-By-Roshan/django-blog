from django.shortcuts import render, redirect, HttpResponse
from .models import Blog, Comment, Subscribe
from .forms import Userregister, BlogForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


def home(request):
    blogs = Blog.objects.all().order_by('-timestamp')
    params = {'blogs': blogs, 'title': 'Home'}
    return render(request, 'home.html', params)


def detail(request, pk):
    blogpost = Blog.objects.filter(pk=pk)
    blogs = Blog.objects.filter(pk=pk).first()
    blogs.views = blogs.views + 1
    blogs.save()
    comments = Comment.objects.filter(post=blogs).order_by('-timestamp')
    categoryId = Blog.objects.filter(pk=pk).values('category')
    categoryNo = categoryId[0].get('category')
    suggestions = Blog.objects.filter(category=categoryNo)
    contex = {'title': 'fullpost', 'blogs': blogpost,
              'comments': comments, 'suggestions': suggestions}
    return render(request, 'details.html', contex)

def comments(request):
    if request.method == 'POST':
        user = request.user
        post = int(request.POST['hidden'])
        cmt = request.POST['cmt']
        blog = Blog.objects.get(id=post)
        blogcmt = Comment(user=user, post=blog, comment=cmt)
        blogcmt.save()
        messages.success(request, "You Have Successfully Posted a Comment")
    return redirect(f'detail/{post}')

def subscribe(request):
    if request.method == 'POST':
        emails = request.POST['subscribe']
        subs = Subscribe(email = emails)
        subs.save()
        messages.success(request, 'You have subscribed to our blog. Now you will get latest information about it.')
        posts = int(request.POST['hiddens'])
    return redirect(f'detail/{posts}')

@login_required(login_url='/login')
def add_view(request):
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
    params = {'form':form, 'title':'Add-Blog'}
    return render(request, 'addblog.html', params)


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
    params = {'searchblogs':searchblog}
    return render(request, 'search.html', params)

def contact(request):
    params = {'title':'Contact'}
    return render(request, 'contact.html')

def managecontact(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        contactmessage = request.POST.get('contactmessage')
        send_mail('Blog message', 
        f"{contactmessage}\n\n {email}",
        email,
        ['pokhrelroshan224@gmail.com'],
        fail_silently=False
        )
        messages.success(request, 'Your Email Has Successfully sent to your admin')
    return redirect(contact)

def login_page(request):
    return render(request, 'login.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['login-email']
        password = request.POST['login-pswd']
        user = authenticate(username=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(
                request, 'you have successfully login into your account')
        else:

            messages.error(
                request, 'user name and password didnot match. try again ')
    return redirect(home)


@login_required(login_url='/login')
def logout_view(request):
    auth_logout(request)
    return redirect('/')


def signUp_view(request):
    if request.method == 'POST':
        form = Userregister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            form.save()
            messages.success(
                request, f"You have successfully registered as {username} ")
    else:
        form = Userregister()
    params = {'form': form, 'title': 'SignUp'}
    return render(request, 'signup.html', params)

@login_required(login_url='/login')
def edit(request, id):
    edit_blog = Blog.objects.get(pk=id)
    form = BlogForm(request.POST, request.FILES, instance= edit_blog)
    if form.is_valid():
        form.save()
        messages.success(
                request, f"Your Post Has Successfully Edited. ")
    else:
        form = BlogForm(instance=edit_blog)
    params = {'form':form}
    
    return render(request, 'editblog.html', params)

@login_required(login_url='/login')
def delete(request):
    if request.method == 'POST':
        delete_item_id = request.POST['delete-id']
        delete_item = Blog.objects.filter(pk = delete_item_id)
        delete_item.delete()
        messages.success(
                request, f"Your post has been deleted. ")
        
    return redirect(home)