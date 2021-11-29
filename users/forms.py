from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from captcha.fields import CaptchaField, CaptchaTextInput

from users.models import Contact, Profile


class RegisterUserForm(UserCreationForm):
    """Registration form."""
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Логин'})
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'})
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Повтор пароля'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    """Login form."""
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'placeholder': 'Логин'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'})
    )


class ContactForm(forms.ModelForm):
    """Contact form."""
    captcha = CaptchaField()

    class Meta:
        model = Contact
        fields = ('name', 'email', 'message', 'captcha')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'message': forms.Textarea(attrs={'placeholder': 'Сообщение'}),
            'captcha': CaptchaTextInput(attrs={'placeholder': 'Captcha'})
        }


class ChangeProfileForm(forms.ModelForm):
    """Change profile information form."""
    class Meta:
        model = Profile
        fields = ('photo', 'bio', 'birthday', 'city')
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }


class ChangeUserForm(forms.ModelForm):
    """Change user information form."""
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
