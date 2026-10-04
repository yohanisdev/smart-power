from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django import forms


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, label='Full name', required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Jane Cooper', 'autocomplete': 'name'}))
    email = forms.EmailField(label='Email address', required=True,
                             widget=forms.EmailInput(attrs={'placeholder': 'jane@example.com', 'autocomplete': 'email'}))

    class Meta(UserCreationForm.Meta):
        fields = ('first_name', 'username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['username'].help_text = 'Letters, digits and @/./+/-/_ only.'
        self.fields['username'].widget.attrs.update({'placeholder': 'Choose a username', 'autocomplete': 'username'})
        self.fields['password1'].label = 'Password'
        self.fields['password1'].widget.attrs.update({'placeholder': 'Create a password', 'autocomplete': 'new-password'})
        self.fields['password2'].label = 'Confirm password'
        self.fields['password2'].widget.attrs.update({'placeholder': 'Re-enter your password', 'autocomplete': 'new-password'})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    next_page = reverse_lazy('dashboard')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class RegisterView(View):
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created successfully.')
            return redirect('dashboard')
        return render(request, self.template_name, {'form': form})


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})
