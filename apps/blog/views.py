from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User

from apps.blog.forms import RegistrationForm
from apps.blog.models import Post

def index(request):
    posts = Post.objects.filter(published=True)
    c = {'posts': posts, 'user': request.user}
    return render(request, 'blog/index.html', c)
 
def post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post.html', {'post': post})

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/blog/')

def register_page(request):
    c = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'])
            return HttpResponseRedirect('/blog/')
        else:
            c.update({'error': 'Invalid form. Try again.'})
    c.update({'form': RegistrationForm()})
    return render(request, 'registration/register.html', c)

