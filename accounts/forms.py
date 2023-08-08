from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, SEX, EmployeeProfile, Company
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'username',
            'id': 'validationCustom08'
        }
    ))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'name': 'password',
            'id': 'validationCustom09'
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']

            if not authenticate(username=username, password=password):
                raise forms.ValidationError('Email and password did not match any user in our database')


class UserRegistrationForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'first_name',
        }
    ))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'last_name',
        }
    ))

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'name': 'email',
        }
    ))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'name': 'password',
            'minlength': "8",
        }
    ))
    password2 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'name': 'password',
            'minlength': "8",
        }
    ))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords dont match')


class UserUpdateForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'first_name',
            'placeholder': "Enter First Name"
        }
    ))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'last_name',
            'placeholder': "Enter Last Name"
        }
    ))

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password1"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password2"].widget = forms.PasswordInput(attrs={"class": "form-control"})



class CompanyForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'first_name',
        }
    ))

    class Meta:
        model = Company
        fields = ('name',)



class EmployeeProfileForm(forms.ModelForm):

    role = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))

    id_number = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }
    ))
    
    sex = forms.ChoiceField(choices=SEX, widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    class Meta:
        model = EmployeeProfile
        fields = ('role', 'id_number', 'sex')