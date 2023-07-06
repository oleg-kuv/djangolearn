from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group, Permission
from django.http import HttpResponseForbidden
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
    post_qs = get_object_or_404(Post, pk=pk)
    tags_qs = post_qs.tags.filter(active=True)
    return render(request, template, {'post': post_qs, 'tags': tags_qs})


@permission_required('blog.add_post')
def post_new(request):
    """ Создание поста """

    template = 'blog/post_edit.html'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post_qs = form.save(commit=False)
            post_qs.author = request.user
            post_qs.save()
            return redirect('post_detail', pk=post_qs.pk)
    else:
        form = PostForm()
    return render(request, template, {'form': form})


@permission_required('blog.change_post')
def post_edit(request, pk):
    """ Редактирование поста """

    template = 'blog/post_edit.html'
    post_qs = get_object_or_404(Post, pk=pk)
    if (request.user != post_qs.author):
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post_qs)
        if form.is_valid():
            post_qs = form.save(commit=False)
            post_qs.author = request.user
            post_qs.save()
            return redirect('post_detail', pk=post_qs.pk)
    else:
        form = PostForm(instance=post_qs)
    return render(request, template, {'form': form})
