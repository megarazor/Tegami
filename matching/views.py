from django.shortcuts import render, get_object_or_404, redirect
from userController.models import Profile
from django.contrib.auth.models import User
from .models import PalList
from django.contrib.auth.decorators import login_required

@login_required
def current_pals(request):
    current_profile= Profile.objects.get(user=request.user)
    pal_list = PalList.objects.get_or_create(profile=current_profile)
    context= {'pal_list': pal_list}
    return render(request, 'matching/current.html', context)

@login_required
def add_or_remove_pals(request, username, verb):
    n_p = get_object_or_404(User, username=username)
    owner = request.user.userprofile
    new_pal = Profile.objects.get(user=n_p)

    if verb == "add":
        new_pal.followers.add(owner)
        PalList.make_pal(owner, new_pal)
    else:
        new_pal.followers.remove(owner)
        PalList.remove_pal(owner, new_pal)

    return redirect(new_pal.get_absolute_url())
