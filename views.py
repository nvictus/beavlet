from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

def login(request):
    return render(request, 'login.html')

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user) #set login status to logged in
        return redirect('/accounts/loggedin')
    else:
        return redirect('/accounts/invalid')

def loggedin(request):
    return render(request, 'loggedin.html', 
        {'full_name': request.user.username})

def invalid_login(request):
    return render(request, 'invalid.html')

def logout(request):
    auth.logout(request)
    return render(request, 'logout.html')

def register_user(request):
    error = None
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/register_success')
        else:
            error = 'Invalid form'
    return render(request, 'register.html', 
        {'form': UserCreationForm(), 'error': error})

def register_success(request):
    return render(request, 'register_success.html')
