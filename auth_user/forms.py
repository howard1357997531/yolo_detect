from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

def validate_email(value):
    # value 是使用者註冊時輸入的電子郵件
    if User.objects.filter(email=value).exists():
        raise ValidationError("電子郵件已被使用", params = {'value': value})

class RegisterForm(UserCreationForm):
    email = forms.EmailField(validators=[validate_email])
    #email = forms.EmailField(widget={'class': 'asd'},validators=[validate_email])
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(),
            'first_name': forms.TextInput(attrs={'required': True}),
            #'email': forms.EmailInput(attrs={'class', 'email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})
        self.fields['email'].widget.attrs.update({'class': 'email'})
        self.fields['password1'].widget.attrs.update({'class': 'password'})
        self.fields['password2'].widget.attrs.update({'class': 'password'})

def validate_profile_email(value):
    # value 是使用者註冊時輸入的電子郵件
    if User.objects.filter(email=value).exists():
        raise ValidationError("電子郵件已被使用", params = {'value': value})
    
class ProfileForm(forms.ModelForm):
    #email = forms.EmailField(validators=[validate_profile_email])

    class Meta:
        model = Profile
        fields = ('name', 'email', 'image')

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(validators=[validate_email])

    class Meta:
        model = User
        fields = ('username', 'email')
