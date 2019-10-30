from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        print("Registration saving...")
        instance = super(UserRegisterForm, self).save(commit=False)

        instance.first_name, instance.last_name = self.cleaned_data['username'].split('.')
        # instance.is_staff = True
        # instance.is_active = False
        if commit:
            instance.save()
        return instance

    def clean_username(self):
        username = self.cleaned_data.get('username', "")
        if username != "" :
            result = username.find('.')
            if result == -1:
                raise forms.ValidationError("Username must contains '.'  Ex: Justin.lee")    
            
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        
        return username


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
