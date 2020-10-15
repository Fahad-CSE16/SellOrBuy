from django import forms
from django.forms import ModelForm, DateInput
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from .fields import ListTextWidget


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email address is already in use.")
        else:
            return email
class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address', 'phone','category','image']
        widgets = {
            'user': forms.HiddenInput(),
            'address': forms.TextInput(attrs={'placeholder': 'Enter your Address'}),
            'category': forms.CheckboxSelectMultiple(attrs={'multiple': True}),
            
        }
        
