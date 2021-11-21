from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from users.forms import LoginUserForm, RegisterUserForm, ContactForm, ChangeUserForm, ChangeProfileForm
from users.models import Contact, Profile
from serials.models import TVSeries


class UserRegisterView(CreateView):
    """Register user."""
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class UserEditView(UpdateView):
    """Update user information."""
    model = User
    form_class = ChangeUserForm
    template_name = 'users/edit_user.html'
    success_url = reverse_lazy('home')


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


class ProfileEditView(UpdateView):
    """Update user profile information."""
    model = Profile
    form_class = ChangeProfileForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_slug_field(self):
        """Get the name of a slug field to be used to look up by slug."""
        return 'user__username'


class UserFavoriteSerials(ListView):
    model = TVSeries
    template_name = 'users/favorite.html'
    context_object_name = 'user_favorites'

    def get_queryset(self):
        return TVSeries.objects.filter(favorite=self.request.user)
