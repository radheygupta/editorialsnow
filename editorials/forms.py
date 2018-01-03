from django import forms
from django.contrib.auth.models import User

from .models import Profile


class RegistrationForm(forms.Form):
    TITLE_CHOICES = [('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Mrs.', 'Mrs.')]
    title = forms.CharField(required=True,
                            widget=forms.Select(attrs={'class': 'custom-select'},
                                                choices=TITLE_CHOICES),
                            max_length=5)
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'myfieldclass'}), max_length=100)
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=150)
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}), min_length=8)

    def clean_email(self):

        if User.objects.filter(username=self.cleaned_data['email']).exists():
            raise forms.ValidationError(('User alredy exists : %(value)s'),
                code='invalid',
                params={'value': self.cleaned_data['email']},
            )
        else:
            return self.cleaned_data['email']


    def save(self, commit=True):
        first_name, last_name = (self.cleaned_data['name'].split(" ", 1) + [None])[:2]
        if last_name:
            return User.objects.create_user(username=self.cleaned_data['email'],
                                            email=self.cleaned_data['email'],
                                            password=self.cleaned_data['password'],
                                            first_name=first_name,
                                            last_name=last_name)
        else:
            return User.objects.create_user(username=self.cleaned_data['email'],
                                            email=self.cleaned_data['email'],
                                            password=self.cleaned_data['password'],
                                            first_name=first_name)


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=150)
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}), min_length=8)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('address', 'birth_date')
