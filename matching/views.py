from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from userController.models import Profile, Notifications
from django.contrib.auth.models import User
from .models import PalList, MatchRequest
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def current_pals(request):
    current_profile= Profile.objects.get(user=request.user)
    pal_list, created = PalList.objects.get_or_create(profile=current_profile)
    p_list= pal_list.pal_list.all()
    context= {'pal_list': p_list}
    return render(request, 'matching/current.html', context)

@login_required
def matching(request, country, gender, min_age, max_age):
    matches= Profile.objects.exclude(user=request.user)
    print("*** QUERY: ", country, gender, min_age, max_age)
    print("*** ", matches)
    if country != '--':
        print("*** Filtering country....")
        matches= matches.filter(country=country)
    print("*** ", matches)
    if gender != '2':
        print("*** Filtering gender....")
        matches= matches.filter(gender=gender)
    print("*** ", matches)
    age_exclude= []
    today=datetime.date.today()
    print("*** Filtering age....")
    for match in matches:
        born= match.DoB
        age= today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        print("Age: ", age)
        if (age < min_age) or (age > max_age):
            age_exclude.append(match.id)
    matches= matches.exclude(id__in=age_exclude)
    print("*** ", matches)
    context= {'matches': matches}
    return render(request, 'matching/results.html', context)

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

@login_required
def matching_confirm(request, username):
    user= User.objects.get(username=username)
    profile= Profile.objects.get(user=user)
    context= {'profile': profile}
    return render(request, 'matching/request_confirm.html', context)

def send_notification(dst_username, content, url):
    user= User.objects.get(username=dst_username)
    new_noti= Notifications(
        user=user, 
        time=datetime.datetime.now(), 
        content= content, 
        read=False, 
        url= url)
    new_noti.save()
    user.notifications.add(new_noti)

@login_required
def send_match_request(request, username):
    requester= Profile.objects.get(user=request.user)
    receiver_user= User.objects.get(username=username)
    receiver= Profile.objects.get(user=receiver_user)
    match_request= MatchRequest.create(requester=requester, receiver=receiver)
    match_request.save()
    send_notification(username, requester.user.username + " sent you a match request.", "/account/profile/" + requester.user.username)
    context= {'receiver': receiver}
    return render(request, 'matching/request_sent.html', context)

@login_required
def respond_match_request(request, request_id, verb):
    try:
        match_request= MatchRequest.objects.get(id=request_id)
    except MatchRequest.DoesNotExist:
        raise Http404("MatchRequest does not exist.")
    owner= request.user.profile
    if verb == 'accept':
        PalList.make_pal(owner, match_request.requester)
        send_notification(
            match_request.requester.user.username, 
            match_request.receiver.user.username + " has accepted your Pen Pal request.",
            "/account/profile/" +  match_request.receiver.user.username)
        match_request.delete()
    else:
        send_notification(
            match_request.requester.user.username, 
            match_request.receiver.user.username + " has declined your Pen Pal request.",
            "/account/profile/" +  match_request.receiver.user.username)
        match_request.delete()
    return redirect('current_pals')

@login_required
def matching_query(request):
    if request.method == 'POST':
        country = request.POST['country']
        gender = request.POST['gender']
        min_age = request.POST['min_age']
        if min_age == '':
            min_age= 18
        max_age = request.POST['max_age']
        if max_age == '':
            max_age= 150
        return redirect('matching', country, gender, min_age, max_age)
    return render(request, 'matching/query.html')

@login_required
def matching_remove(request, username):
    current_profile= request.user.profile
    target_user= User.objects.get(username=username)
    target_profile= target_user.profile
    PalList.remove_pal(current_profile, target_profile)
    PalList.remove_pal(target_profile, current_profile)
    return redirect('current_pals')

@login_required
def matching_remove_confirm(request, username):
    try:
        target_user= User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User with that username does not exist.")
    target_profile= target_user.profile
    context= {'profile': target_profile}
    return render(request, 'matching/remove_confirm.html', context)