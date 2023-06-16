from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm


def post_list(request):
    """ Список постов """

    template = 'blog/post_list.html'
    filter_active = request.GET.get('active', True)

    posts_qs = Post.objects.order_by(
        'created_date').filter(active=filter_active)

    if filter_tag := request.GET.get('tag'):
        posts_qs = posts_qs.filter(tags=filter_tag)

    return render(request, template, {'posts': posts_qs})


def post_detail(request, pk):
    """ Страница поста """

    template = 'blog/post_detail.html'
    post = get_object_or_404(Post, pk=pk)
    tags = post.tags.filter(active=True)
    return render(request, template, {'post': post, 'tags': tags})


@login_required
def post_new(request):
    """ Создание поста """

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    """ Редактирование поста """

    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
