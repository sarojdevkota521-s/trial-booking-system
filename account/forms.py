from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# from .models import Profile

# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['phone', 'address', 'bio', 'profile_image']

class RegisterForm(UserCreationForm):
        class Meta:
            model = User
            fields = ["first_name", "last_name","username", "email", "password1", "password2"]
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for field in self.fields.values():
                field.widget.attrs.update({
                        'class': 'input-field',
                        'required': 'required'
                    })