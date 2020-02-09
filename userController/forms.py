from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile

CHOICES= [('--', 'None'), ('en', 'English'), ('ja', '日本語'), ('vi', 'Tiếng Việt')]
LANGUAGE_CODE= {'--': 'None', 'en': 'English', 'ja': '日本語', 'vi': 'Tiếng Việt'}

class ExtendedUserCreationForm(UserCreationForm):
    email= forms.EmailField(required=True)
    first_name= forms.CharField(max_length=50)
    last_name= forms.CharField(max_length=50)

    class Meta:
        model= User
        fields= ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user= super().save(commit=False)
        user.email= self.cleaned_data['email']   
        user.first_name= self.cleaned_data['first_name']    
        user.last_name= self.cleaned_data['last_name']
        
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    language1= forms.ChoiceField(choices=CHOICES)
    language2= forms.ChoiceField(choices=CHOICES)
    language3= forms.ChoiceField(choices=CHOICES)
    language4= forms.ChoiceField(choices=CHOICES)
    language5= forms.ChoiceField(choices=CHOICES)
    class Meta:
        model= Profile
        fields= ('DoB', 'gender', 'country', 'address', 'intro', 'profile_pic') 

class ExtendedUserEditionForm(UserChangeForm):
    email= forms.EmailField(required=True)
    first_name= forms.CharField(max_length=50)
    last_name= forms.CharField(max_length=50, required=True)

    class Meta:
        model= User
        fields= ('email', 'first_name', 'last_name')
