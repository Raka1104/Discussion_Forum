from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile, Post, Replie
from json import dumps
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages





# Create your views here.
@login_required(login_url = '/login')
def forum(request):

# Get the list of projects

    try:
        user = get_object_or_404(User, username=request.user)
        profile = get_object_or_404(Profile, user=user)
    except:
       user = None
       profile = None
    if request.method=="POST":
        user = request.user
        image = request.user.profile.image
        content = request.POST.get('content','')
        post = Post(user=user, post_content=content, image=image)
        post.save()
        alert = True
        return render(request, "forum.html", {'alert':alert, 'msg': 'Your question has been posted successfully!!!'})
    posts = Post.objects.filter().order_by('-timestamp')
    spost = []
    if profile:
        spost = [None]*posts.count()
        psposts = profile.get_saved_post()
        for index, data in enumerate(posts):
            if psposts.__contains__(data):
                spost[index] = True
            else:
                spost[index] = False

    return render(request, "forum.html", {'posts':posts, 'spost':dumps(spost)})

def savePost(request, myid):
    user = get_object_or_404(User, username=request.user)
    profile = get_object_or_404(Profile, user=user)
    post = Post.objects.filter(id=myid).first()
    if profile.get_saved_post().__contains__(post):
       profile.remove_post(post)
    else:
       profile.save_post(post)
    profile.save()
    return redirect("/")

def edit(request, myid):
    user = request.user
    post = Post.objects.filter(id=myid).first()
    replies = Replie.objects.filter(post=post)
    if request.method=="POST":
      if post.user == user:
        post.post_content = request.POST.get('content','')
        post.save()
        alert = True
        return render(request, "discussion.html", {'alert':alert, 'id':post.id, 'msg': 'Your post has been edited successfully!!!'})
      else:
        alert = True
        return render(request, "discussion.html", {'alert':alert, 'id':post.id, 'msg': 'You are not authorised to edit this post!!!'})
    return render(request, "discussion.html", {'post':post, 'replies':replies})

def editPost(request, myid):
    user = request.user
    post = Post.objects.filter(id=myid).first()
    if request.method=="POST":
      if post.user == user:
        post.post_content = request.POST.get('content','')
        post.save()
        alert = True
        return render(request, "forum.html", {'alert':alert, 'msg': 'Your post has been edited successfully!!!'})
      else:
        alert = True
        return render(request, "forum.html", {'alert':alert, 'msg': 'You are not authorised to edit this post!!!'})
    return render(request, "forum.html", {'post':post})

def editReply(request, myid):
    user = request.user
    reply = Replie.objects.filter(id=myid).first()
    post = reply.post
    if request.method=="POST":
      if reply.user == user:
        reply.reply_content = request.POST.get('content','')
        reply.save()
        alert = True
        return render(request, "discussion.html", {'alert':alert, 'id':post.id, 'msg': 'Your reply has been edited successfully!!!'})
      else:
        alert = True
        return render(request, "discussion.html", {'alert':alert, 'id':post.id, 'msg': 'You are not authorised to edit this reply!!!'})
    replies = Replie.objects.filter(post=post)
    return render(request, "discussion.html", {'post':post, 'replies':replies})

def deleteReply(request, myid):
    user = request.user
    reply = Replie.objects.filter(id=myid).first()
    post = reply.post
    if request.method=="POST":
      if reply.user == user:
        reply.delete()
        alert = True
        return render(request, "discussion.html", {'alert':alert, 'id':post.id, 'msg': 'Your reply has been deleted successfully!!!'})
      else:
        alert = True
        return render(request, "discussion.html", {'alert':alert, 'id':post.id, 'msg': 'You are not authorised to delete this reply!!!'})
    replies = Replie.objects.filter(post=post)
    return render(request, "discussion.html", {'post':post, 'replies':replies})

def delete(request, myid):
    user = request.user
    post = Post.objects.filter(id=myid).first()
    replies = Replie.objects.filter(post=post)
    if request.method=="POST":
      if post.user == user:
        post.delete()
        dalert = True
        return render(request, "discussion.html", {'dalert':dalert, 'msg': 'Your post has been deleted successfully!!!'})
      else:
        alert = True
        return render(request, "discussion.html", {'alert':alert, 'id':post.id, 'msg': 'You are not authorised to delete this post!!!'})
    return render(request, "discussion.html", {'post':post, 'replies':replies})

def deletePost(request, myid):
    user = request.user
    post = Post.objects.filter(id=myid).first()
    if request.method=="POST":
      if post.user == user:
        post.delete()
        alert = True
        return render(request, "forum.html", {'alert':alert, 'msg': 'Your post has been deleted successfully!!!'})
      else:
        alert = True
        return render(request, "forum.html", {'alert':alert, 'msg': 'You are not authorised to delete this post!!!'})
    return render(request, "forum.html", {'post':post})

@login_required(login_url='/login')
def discussion(request, myid):
    user = request.user
    try:
       profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
       profile= None   

    post = Post.objects.filter(id=myid).first()
    replies = Replie.objects.filter(post=post)

    if request.method=="POST":
        user = request.user
        image = request.user.profile.image
        desc = request.POST.get('desc','')
        reply = Replie(user = user, reply_content = desc, post=post, image=image)
        reply.save()
        alert = True
        return render(request, "discussion.html", {'alert':alert, 'id':post.id, 'msg': 'Your reply has been posted successfully!!!'})
    return render(request, "discussion.html", {'post':post, 'replies':replies})

def userLogin(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials")

    
    return render(request, "login.html")

def userLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out", extra_tags='logout')
    return redirect('/login')

def userRegister(request):
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        try:
            validate_password(password)
        except Exception as e:
            context = {'error_message': ''.join(e)}
            return render(request, 'register.html', context)
        
        if len(username) > 15:
            context = {'error_message': "Username must be under 15 characters."}
            return render(request, 'register.html', context)
        if not username.isalnum():
            context = {'error_message': "Username must contain only letters and numbers."}
            return render(request, 'register.html', context)
        if password != confirm_password:
            context = {'error_message': "Passwords do not match."}
            return render(request, 'register.html', context)
        
        try: 
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            profile = Profile(user=user, bio="")
            profile.save()

            return render(request, 'login.html') 
        except IntegrityError:
           context= {'error_message': "Username already exists. Please choose a different username."}
           return render(request, 'register.html', context)
        
    return render(request, "register.html")

@login_required(login_url = '/login')
def myprofile(request):
    user = get_object_or_404(User, username=request.user)
    profile = get_object_or_404(Profile, user=user)

# request.user - gets the username from the backend
#to get username from the frontend request.POST.get('username', '')

    if request.method=="POST":
        user = request.user    
        user = get_object_or_404(User, username=request.user)
        profile = get_object_or_404(Profile, user=user)


        fname = request.POST.get('fname','')
        lname = request.POST.get('lname','')
        bio = request.POST.get('bio','')
        email = request.POST.get('email','')
        prf = request.POST.get('prf','')
        user.first_name = fname
        user.last_name = lname
        user.email = email
        user.save()
        profile.user = user
        profile.bio = bio
        profile.image = request.FILES.get('imgfile',)
        profile.save()
        return render(request, "profile.html", {'profile':profile})
    return render(request, "profile.html", {'profile':profile})

@login_required(login_url = '/login')
def userProfile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, "userProfile.html", {'userProfile': profile})
