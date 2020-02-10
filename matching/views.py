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

    ages= []
    countries= []
    for p in p_list:
        ages.append(p.get_age())
        countries.append(p.country_get_as_string())
    p_list_detailed= zip(p_list, ages, countries)
    print(p_list)
    context= {'pal_list': p_list_detailed}
    return render(request, 'matching/current.html', context)

@login_required
def matching(request, country, gender, min_age, max_age, lang_list):
    matches= Profile.objects.exclude(user=request.user)
    if country != '--': # Filter by country
        matches= matches.filter(country=country)
    if gender != '2': # Filter by gender
        matches= matches.filter(gender=gender)
    to_be_exclude= []
    # today=datetime.date.today()
    current_profile= request.user.profile
    if (lang_list != 'none'):
        query_lang_list= lang_list.split(",")
        for match in matches:
            # Filter by age range
            # Filter out people who are already pals
            # Filter by languages
            # born= match.DoB
            # age= today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            match_lang_list= match.languages_get_as_list()
            age= match.get_age()
            if (age < min_age) or (age > max_age):
                to_be_exclude.append(match.id)
            elif not any(lang in query_lang_list for lang in match_lang_list):
                # print("**** NOT COMMON")
                # print("query_lang_list: ", query_lang_list)
                # print("match_lang_list: ", match_lang_list)
                to_be_exclude.append(match.id)
            elif PalList.is_pal(current_profile, match):
                to_be_exclude.append(match.id)
    else:
        for match in matches:
            # Filter by age range
            # Filter out people who are already pals
            # born= match.DoB
            # age= today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            match_lang_list= match.languages_get_as_list()
            age= match.get_age()
            if (age < min_age) or (age > max_age):
                to_be_exclude.append(match.id)
            elif PalList.is_pal(current_profile, match):
                to_be_exclude.append(match.id)
    matches= matches.exclude(id__in=to_be_exclude)
    ages= []
    countries= []
    for match in matches:
        ages.append(match.get_age())
        countries.append(match.country_get_as_string())
    matches_n_ages= zip(matches, ages, countries)
    context= {'matches': matches_n_ages}
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
        lang_list= ""
        if request.POST['language1'] != '--':
            lang_list+= request.POST['language1'] + ','
        if request.POST['language2'] != '--':
            lang_list+= request.POST['language2'] + ','
        if request.POST['language3'] != '--':
            lang_list+= request.POST['language3'] + ','
        if request.POST['language4'] != '--':
            lang_list+= request.POST['language4'] + ','
        if request.POST['language5'] != '--':
            lang_list+= request.POST['language5'] + ','
        if lang_list == "":
            lang_list= 'none'
        else:
            lang_list= lang_list[:-1]
        return redirect('matching', country, gender, min_age, max_age, lang_list)
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

