from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Email already exists")
        return email

    def full_clean(self):
        super().full_clean()

        uniq_error = False

        # Check if username error exists
        if 'username' in self.errors:
            username_errors = self.errors['username']
            if any('A user with that username already exists.' in str(error) for error in username_errors):
                # Remove the username error
                del self.errors['username']
                uniq_error = True


        # Check if email error exists
        if 'email' in self.errors:
            email_errors = self.errors['email']
            if any('Email already exists' in str(error) for error in email_errors):
                # Remove the email error
                del self.errors['email']
                uniq_error = True

        if uniq_error:
            self.add_error(None, "A user with the given email address or username already exists")

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
