from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)

        user.is_active = False

        if commit:
            user.save()

        return user

class DeleteForm(forms.Form):
    confirm = forms.BooleanField(
        label='I understand that by deleting my account, all related data will be permanently deleted.',
        required=True
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        required=True
    )
