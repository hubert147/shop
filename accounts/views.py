from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from accounts.forms import LoginForm, UserCreateForm


from django.contrib.auth.models import User

# Create your views here.
class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'form_generic.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
            form = LoginForm()
        return render(request, 'form_generic.html', {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('index')


class UserCreateView(CreateView):

    model = User
    form_class = UserCreateForm
    template_name = 'form_generic.html'
    success_url = reverse_lazy('index')

