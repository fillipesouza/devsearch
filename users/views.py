from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .utils import search_profiles, paginate_profiles
from .models import Profile, Message
from .forms import CustomUserCreationForm, MessageForm, ProfileForm, SkillForm, MessageForm
from django.contrib.auth.models import User


# Create your views here.

def login_user(request):

    page = 'login'

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
            return redirect('login')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, 'User successfully logged')
            return redirect(request.GET['next'] if 'next' in request.GET else 'profiles')
        else:
            print('Username or password incorrect')

    context = { 'page': page }

    return render(request, 'users/login-page.html', context)
            

def register_user(request):

    page = 'register'

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
        
            login(request, user)
            messages.success(request, 'User successfully registered')
            return redirect('profiles')
        else:
            messages.success(request, 'Bad registration')

    form = CustomUserCreationForm()
    context = { 'page': page, 'form': form }

    return render(request, 'users/login-page.html', context)

def logout_user(request):
    logout(request)
    messages.success(request,'User succesfully logged out')
    return redirect('login')
        

def profiles(request):
    profiles, search_query = search_profiles(request)
    custom_range, profiles = paginate_profiles(request, profiles, results=2)
    context = {'profiles': profiles,  'search_query': search_query, 'custom_range': custom_range }
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(description__exact='')
    other_skills = profile.skill_set.filter(description='')
    context = {'profile': profile, 'top_skills': top_skills, 'other_skills': other_skills }
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    context = {'profile': profile, 'skills': skills }
    return render(request, 'users/user-account.html', context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.username = profile.username.lower()
            profile.save() 
            messages.success(request, 'User successfully registered')
            return redirect('profiles')
        else:
            messages.success(request, 'Bad registration')

    context = { 'form': form }

    return render(request, 'users/profile-form.html', context)


@login_required(login_url='login')
def add_skill(request):
    form = SkillForm()
    profile = request.user.profile
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        #print(request.POST) - logging request
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        #print(request.POST) - logging request
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')

    context = {'form': form }
    return render(request, 'users/skill-form.html', context)

@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        #print(request.POST) - logging request
        if form.is_valid():
            skill.delete()
            return redirect('account')

    context = { 'object': skill }
    return render(request, 'projects/delete-form.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    message_requests = profile.messages.all()
    unread_messages = message_requests.filter(is_read=False).count()
    context = { 'message_requests': message_requests, 'unread_messages':unread_messages }
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def read_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = { 'message': message }
    return render(request, 'users/message.html', context )
    

def send_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    try:
        sender = request.user.profile
    except:
        sender = None
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        #print(request.POST) - logging request
        if form.is_valid():
            message = form.save(commit=False)
            message.recipient = recipient
            if sender:
                message.email = sender.email
                message.sender = sender
                message.name = sender.name
            message.save()
        messages.success(request, 'Message successfully sent')
        return redirect('user-profile', recipient.id)

    context = {'form': form}
    return render(request, 'users/message-form.html', context)

