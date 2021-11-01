from django.shortcuts import redirect
from django.views.generic import CreateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.core.mail import send_mail

from users.forms import LoginUserForm, RegisterUserForm, ContactForm
from users.models import Contact


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class ContactFormView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'users/contact.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        return redirect('home')
