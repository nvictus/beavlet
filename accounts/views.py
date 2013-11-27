from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def login(request):
    """
    A GET query parameter 'next' may be provided, designating where to redirect
    after authentication (provided by views with the @login_required decorator).

    Presents: 
        - login form, to be submitted to auth_view.

    """
    return render(request, 'accounts/login.html', 
        {'next': request.GET.get('next', '')})

def auth_view(request):
    """
    Login info submitted. The 'next' parameter from the login page is submitted
    here as POST data.

    Redirects: 
        - to confirmation page or landing url specified by 'next'
        - to failure page if authentication fails

    """
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user) #set login status to logged in
        if request.POST['next']:
            return redirect(request.POST['next'])
        return redirect('/accounts/loggedin')
    else:
        return redirect('/accounts/invalid')

def loggedin(request):
    return render(request, 'accounts/loggedin.html', {'full_name': request.user.username})

def invalid_login(request):
    return render(request, 'accounts/invalid.html')

def logout(request):
    """
    Logs user out.

    Presents: logout confirmation

    """
    auth.logout(request)
    return render(request, 'accounts/logout.html')

def register_user(request):
    """
    Registration form.

    Presents: registration form on GET or failed registration
    Redirects: to registration confirmation on successful registration
    """
    error = None
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/register_success')
        else:
            error = 'Invalid form'
    return render(request, 'accounts/register.html', 
        {'form': UserCreationForm(), 'error': error})

def register_success(request):
    return render(request, 'accounts/register_success.html')

@login_required
def profile_view(request):
    user = request.user
    # populate profile page with user data
    render(request, 'accounts/user_profile.html', context)

