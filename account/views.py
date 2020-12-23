from django.shortcuts import render, redirect, reverse
from .forms import LoginForm, UserRegisterationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.

class Login(LoginView):    
    template_name = 'blog/login.html'


class Logout(LogoutView):
    pass


class Register(CreateView, SuccessMessageMixin):
    template_name = 'blog/register.html'
    form_class = UserRegisterationForm
    success_url = '/login/'
    success_message = 'Your account was created successfully.'

# def logout_view(request):
#     logout(request)
#     return redirect('post_archive')


# def register_view(request):
#     if request.method == 'GET':
#         form = UserRegisterationForm()
#     else:
#         form = UserRegisterationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data.get('password'))
#             form.save()
#             return redirect('post_archive')

#     context = {
#         'form': form,
#     }
#     return render(request, 'blog/register.html', context=context)