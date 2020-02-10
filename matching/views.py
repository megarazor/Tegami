from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from userController.models import Profile, Notifications
from django.contrib.auth.models import User
from .models import PalList, MatchRequest
from django.contrib.auth.decorators import login_required
import datetime
from .forms import MatchQueryForm

@login_required
def current_pals(request):
    current_profile= Profile.objects.get(user=request.user)
    pal_list, created = PalList.objects.get_or_create(profile=current_profile)
    p_num= pal_list.pal_list.all().count()
    p_list= pal_list.pal_list.all()

    ages= []
    countries= []
    for p in p_list:
        ages.append(p.get_age())
        countries.append(p.country_get_as_string())
    p_list_detailed= zip(p_list, ages, countries)
    context= {'pal_list': p_list_detailed, 'pal_num': p_num}
    return render(request, 'matching/current.html', context)

@login_required
def matching(request, country, gender, min_age, max_age, lang_list):
    print("*** QUERY: ", country, gender, min_age, max_age, lang_list)
    matches= Profile.objects.exclude(user=request.user)
    if country != '--': # Filter by country
        matches= matches.filter(country=country)
    if gender != '-1': # Filter by gender
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
    matches_num= matches.count()
    ages= []
    countries= []
    for match in matches:
        ages.append(match.get_age())
        countries.append(match.country_get_as_string())
    matches_n_ages= zip(matches, ages, countries)
    context= {'matches': matches_n_ages, 'matches_num': matches_num}
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
        return redirect('current_pals')
    else:
        send_notification(
            match_request.requester.user.username, 
            match_request.receiver.user.username + " has declined your Pen Pal request.",
            "/account/profile/" +  match_request.receiver.user.username)
        match_request.delete()
        return redirect('profile_other', match_request.requester.user.username)
    
@login_required
def matching_query(request):
    if request.method == 'POST':
        query_form= MatchQueryForm(request.POST)
        if query_form.is_valid():
            country = query_form.cleaned_data['country']
            gender = query_form.cleaned_data['gender']
            min_age = query_form.cleaned_data['min_age']
            max_age= query_form.cleaned_data['max_age']
            language1= query_form.cleaned_data['language1']
            language2= query_form.cleaned_data['language2']
            language3= query_form.cleaned_data['language3']
            language4= query_form.cleaned_data['language4']
            language5= query_form.cleaned_data['language5']
            lang_list= ""
            if language1 != '--':
                lang_list+= language1 + ','
            if language2 != '--':
                lang_list+= language2 + ','
            if language3 != '--':
                lang_list+= language3 + ','
            if language4 != '--':
                lang_list+= language4 + ','
            if language5 != '--':
                lang_list+= language5 + ','
            if lang_list == "":
                lang_list= 'none'
            else:
                lang_list= lang_list[:-1]
            return redirect('matching', country, gender, min_age, max_age, lang_list)
        else:
            return redirect('matching_query')
    query_form= MatchQueryForm(initial={'max_age': 150})
    context= {'query_form': query_form}
    return render(request, 'matching/query.html', context)

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

