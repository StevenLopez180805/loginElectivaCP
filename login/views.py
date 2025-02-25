from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
# Create your views here.
def home(request):
  return render(request, 'home.html', {})

def signUp(request):
  if request.method == 'GET':
    return render(request, 'signUp.html', {
    'form': UserCreationForm
    })
  else:
    if request.POST['password1'] == '' or request.POST['password1'] == '' or request.POST['username'] == '':
      return render(request, 'signUp.html', {
        'form': UserCreationForm,
        'error': 'Todos los campos son obligatorios.'
      })
    if request.POST['password1'] == request.POST['password2']:
      try:
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
        user.save()
        login(request, user)
        return redirect('home')
      except IntegrityError:
        return render(request, 'signUp.html', {
        'form': UserCreationForm,
        'error': 'El nombre de usuario ya se encuentra en uso.'
      })
    else:
      return render(request, 'signUp.html', {
        'form': UserCreationForm,
        'error': 'Las contraseñas no coindicen.'
      })

def signOut(request):
  logout(request)
  return redirect('signIn')

def signIn(request):
  if request.method == 'GET':
    return render(request, 'signIn.html', {
      'form': AuthenticationForm
    })
  else:
    if request.POST['password'] == '' or request.POST['username'] == '':
      return render(request, 'signIn.html', {
        'form': AuthenticationForm,
        'error': 'Todos los campos son obligatorios.'
      })
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user is None:
      return render(request, 'signIn.html', {
        'form': AuthenticationForm,
        'error': 'Nombre de usuario y/o contraseña incorrectos.'
      })
    else:
      login(request, user)
      return redirect('home')