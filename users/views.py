from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from blog.models import Article
from serials.models import TVSeries
from users.forms import (
    ChangeProfileForm,
    ChangeUserForm,
    ContactForm,
    LoginUserForm,
    RegisterUserForm,
)
from users.models import Contact, Profile


class UserRegisterView(CreateView):
    """Register user."""
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class UserEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update user information."""
    model = User
    form_class = ChangeUserForm
    template_name = 'users/edit_user.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.get_object().id == self.request.user.id


class LoginUser(LoginView):
    """Login user."""
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    """Logout user."""
    logout(request)
    return redirect('login')


class ContactFormView(SuccessMessageMixin, CreateView):
    """Contact form."""
    model = Contact
    form_class = ContactForm
    template_name = 'users/contact.html'
    success_url = reverse_lazy('home')
    success_message = 'Форма успешно отправлена!'

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class UserProfileView(DetailView):
    """Show user profile information."""
    model = Profile
    template_name = 'users/user_profile.html'
    context_object_name = 'page_user'

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def get_slug_field(self):
        """Get the name of a slug field to be used to look up by slug."""
        return 'user__username'


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update user profile information."""
    model = Profile
    form_class = ChangeProfileForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_slug_field(self):
        """Get the name of a slug field to be used to look up by slug."""
        return 'user__username'

    def test_func(self):
        return self.get_object().user == self.request.user


class UserFavoriteSerials(ListView):
    model = TVSeries
    template_name = 'users/favorite.html'
    context_object_name = 'user_favorites'

    def get_queryset(self):
        return TVSeries.objects.filter(favorite=self.request.user)


class UserLikedArticles(ListView):
    model = Article
    template_name = 'users/liked_articles.html'
    context_object_name = 'user_likes'

    def get_queryset(self):
        return Article.objects.filter(likes=self.request.user)
