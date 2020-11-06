from django.shortcuts import render, get_object_or_404, redirect,HttpResponseRedirect
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django .core.paginator import Paginator, PageNotAnInteger, EmptyPage



def post_index(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date")
    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    # request.GET is a dictionary with GET parameters/variables/query string (every thing after the ? is the query string)
    # .get() is used for dictionaries to retrieve the value of the variable/item.{item : value}, {"page": 3}
    # it's saying "get the value with the GET variable named 'page'"
    try:
        post_list = paginator.page(page)
            # paginator.page() returns the paginated results of a page as an argument
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)
    return render(request, "blog/post_index.html", {"posts": posts, "page": page, "post_list": post_list})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment = post.comments.filter(approved_comment=True)
    return render(request, "blog/post_detail.html", {"post" : post, "comment" : comment})


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user                    # these fields are required to be specific info.
            post.published_date = timezone.now()          # the user and time published shouldn't be chosen by the user.
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
        return render(request, "blog/post_create.html", {"form" : form})


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk,)
    if request.method == "POST" and post.author == request.user:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            messages.success(request, "Post Successfully Updated!")
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, "blog/post_update.html", {"form" : form})
    

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST" and post.author == request.user:
        post.delete()
        messages.success(request, "Post Successfully Deleted!")
        return redirect("post_index")
    else:
        return render(request, "blog/post_confirm_delete.html", {"post" : post})