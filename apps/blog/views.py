from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from apps.blog.models import Post

def index(request):
    posts = Post.objects.filter(published=True)
    c = {'posts': posts, 'user': request.user}
    return render(request, 'blog/index.html', c)
 
def post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post.html', {'post': post})
