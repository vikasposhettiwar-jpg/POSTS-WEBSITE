from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,PostForm
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# 1) funcions 2)classes


def home(request):
    name = 'Vikas'
    nums=[1,2,3,4,5]
    context = {'name':name,'nums':nums}
    return render(request,'home.html',context)

def user_login(request):
     if request.method =='GET':
        return render(request,'login.html')
     
     if request.method =='POST':
         username = request.POST.get('username')
         password = request.POST.get('password')

         user = authenticate(request,username=username,password=password)

         if user is not None:
             login(request,user)
             return redirect('home')
         else:
             error='invalid username or password'
             return render(request,'login.html',{'error':error})
         

def register(request):
    form = UserRegistrationForm()

    if request.method =='GET':
        return render(request,'register.html',{'form':form})
    
    if request.method =='POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request,'register.html',{'form':form})
        
def user_logout(request):
    logout(request)
    return redirect('home')

def posts(request):
    return render(request,'posts.html')


def posts(request):
    post_list =Post.objects.all().order_by('-updated_at')
    return render(request,'posts.html',{ 'post_list':post_list})

def read_post(request,id):
    try:
        post=Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return redirect('posts')
       
    return render(request,'read-post.html',{ 'post':post})

@login_required(login_url='login')
def create_post(request):
    form = PostForm()

    if request.method =='GET':
        return render(request,'create-post.html',{'form':form})
    
    if request.method =='POST':
        form = PostForm(request.POST,request.FILES)

        if form.is_valid():
            post=form.save(commit=False)
            post.author= request.user #assign user as author
            post.save() #create post
            return redirect('posts')
        
        else:
            return render(request,'create-post.html',{'form':form})
        
def update_post(request,id):
    try:
        post=Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return redirect('posts')  

    if request.user != post.author:
        return redirect('posts')
    
    form=PostForm(instance=post)

    if request.method=='GET':
        return render(request,'update-post.html',{'form':form})
    
    if request.method=='POST':
        form = PostForm(request.POST, request.FILES,instance=post)
    
    if form.is_valid():
        post = form.save(commit =False)
        post.update_at = timezone.now()
        post.save()
        return redirect('posts')
    else:
        return render(request,'update-post.html',{'form':form})
        

def delete_post(request,id):
    try:
        post=Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return redirect('posts')  
    
    if request.user != post.author:
        return redirect('posts')
    
    post.delete()
    return redirect('posts') 

    

        
  

    


                                        