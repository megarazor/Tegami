from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import ExtendedUserCreationForm, ExtendedUserEditionForm, ProfileForm, LANGUAGE_CODE
from django.contrib.auth.models import User
from .models import Profile
from matching.models import MatchRequest, PalList

def home(request):
    return render(request, 'basic_interface/home.html')

def logging_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request,'Username and password didn\'t match')
            return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def logging_out(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):    
    profile= Profile.objects.get(user=request.user)  
    lang_list= profile.languages_get_as_list()
    lang_list_decoded= []
    for lang in lang_list:
        lang_list_decoded.append(LANGUAGE_CODE[lang])
    context= {'profile': profile, 'lang_list': lang_list_decoded}
    return render(request, 'basic_interface/profile.html', context)

@login_required
def profile_other(request, username):
    if (username == request.user.username):
        return redirect('profile')
    user= User.objects.get(username=username)
    profile= Profile.objects.get(user=user)    
    current_profile= Profile.objects.get(user=request.user)
    try:
        sent_match_request= MatchRequest.objects.get(requester=current_profile, receiver=profile)
    except MatchRequest.DoesNotExist:
        sent_match_request= None
    try:
        received_match_request= MatchRequest.objects.get(requester=profile, receiver=current_profile)
    except MatchRequest.DoesNotExist:
        received_match_request= None
    is_pal= PalList.is_pal(current_profile, profile)
    lang_list= profile.languages_get_as_list()
    lang_list_decoded= []
    for lang in lang_list:
        lang_list_decoded.append(LANGUAGE_CODE[lang])
    context= {
        'profile': profile,
        'sent_request': sent_match_request, 
        'received_request': received_match_request, 
        'is_pal': is_pal,
        'lang_list': lang_list_decoded
        }
    return render(request, 'basic_interface/profile_other.html', context)

def register(request):
    if (request.method=='POST'):
        user_form= ExtendedUserCreationForm(request.POST)
        profile_form= ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            language1= profile_form.cleaned_data['language1']
            language2= profile_form.cleaned_data['language2']
            language3= profile_form.cleaned_data['language3']
            language4= profile_form.cleaned_data['language4']
            language5= profile_form.cleaned_data['language5']
            languages= []
            if language1 != '--':
                languages.append(language1)
            if language2 != '--':
                languages.append(language2)
            if language3 != '--':
                languages.append(language3)
            if language4 != '--':
                languages.append(language4)
            if language5 != '--':
                languages.append(language5)
            if len(languages) == 0:
                messages.error(request, 'Please input at least one language')
                return redirect('register')
            
            user= user_form.save()
            profile= profile_form.save(commit=False)
            profile.user= user
            profile.save()

            Profile.languages_set_from_list(profile, languages)

            username= user_form.cleaned_data.get('username')
            password= user_form.cleaned_data.get('password1')
            user= authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        user_form= ExtendedUserCreationForm()
        profile_form= ProfileForm()
    
    context= {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'basic_interface/register.html', context)

@login_required
def settings(request):
    return redirect('edit_info')

@login_required
def edit_info(request):
    if (request.method=='POST'):
        user_form= ExtendedUserEditionForm(request.POST)
        profile_form= ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            languages= []
            language1= profile_form.cleaned_data['language1']
            language2= profile_form.cleaned_data['language2']
            language3= profile_form.cleaned_data['language3']
            language4= profile_form.cleaned_data['language4']
            language5= profile_form.cleaned_data['language5']
            if language1 != '--':
                languages.append(language1)
            if language2 != '--':
                languages.append(language2)
            if language3 != '--':
                languages.append(language3)
            if language4 != '--':
                languages.append(language4)
            if language5 != '--':
                languages.append(language5)
            if len(languages) == 0:
                messages.error(request, 'Please enter at least one language')
                return redirect('edit_info')
            profile= Profile.objects.get(user=request.user)
            profile.user.email= user_form.cleaned_data.get('email')
            profile.user.first_name= user_form.cleaned_data.get('first_name')
            profile.user.last_name= user_form.cleaned_data.get('last_name')
            profile.gender= profile_form.cleaned_data.get('gender')
            profile.DoB= profile_form.cleaned_data.get('DoB')
            profile.country= profile_form.cleaned_data.get('country')
            profile.intro= profile_form.cleaned_data.get('intro')
            profile.address= profile_form.cleaned_data.get('address')
            profile.profile_pic= profile_form.cleaned_data.get('profile_pic')
            profile.user.save()
            profile.save()
            Profile.languages_set_from_list(profile, languages)
            
            return redirect('profile')
    else:
        user= request.user
        profile= user.profile
        user_form= ExtendedUserEditionForm(initial={
            'email': user.email, 
            'first_name': user.first_name,
            'last_name': user.last_name
            })
        profile_form= ProfileForm(initial={
            'DoB': profile.DoB,
            'gender': profile.gender,
            'country': profile.country,
            'address': profile.address,
            'intro': profile.intro,
            'profile_pic': profile.profile_pic})
    
    context= {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'settings/info.html', context)

@login_required
def edit_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
    
    form= PasswordChangeForm(user=request.user)
    context= {'form': form}
    return render(request, 'settings/password.html', context)

@login_required
def notifications_view(request):
    current_user= request.user
    notifications= current_user.notifications.all()
    for noti in notifications:
        if noti.read==False:
            noti.read=True
            noti.save()
    context= {'notifications': notifications}
    return render(request, 'basic_interface/notifications.html', context)
