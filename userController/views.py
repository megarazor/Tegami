from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import ExtendedUserCreationFrom, ProfileForm
from .models import Profile

def home(request):
    return render(request, 'home.html')

@login_required
def profile(request):
    profile= Profile.objects.get(user=request.user)
    context= {'user': profile}
    return render(request, 'profile.html', context)

def register(request):
    if (request.method=='POST'):
        user_form= ExtendedUserCreationFrom(request.POST)
        profile_form= ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user= user_form.save()
            profile= profile_form.save(commit=False)
            profile.user= user
            profile.save()

            username= user_form.cleaned_data.get('username')
            password= user_form.cleaned_data.get('password')
            user= authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        user_form= ExtendedUserCreationFrom()
        profile_form= ProfileForm()
    
    context= {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'register.html', context)

# def login(request):
#     if (request.method == 'POST'):
#         user = authenticate(username=request.POST['username'], password=request.POST['password'])
#         if user is not None:
#             # A backend authenticated the credentials
#         else:
#             # No backend authenticated the credentials
