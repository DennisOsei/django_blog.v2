from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone



def post_index(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date")
    return render(request, "blog/post_index.html", {"posts" : posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment = get_object_or_404(Comment, pk=post.pk)
    return render(request, "blog/post_detail.html", {"post" : post, "comment" : comment})