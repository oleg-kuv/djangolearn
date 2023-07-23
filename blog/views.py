from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Post, Tag
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
        form = PostForm(request.POST, request.user)
        if form.is_valid():
            post_qs = form.save()
            post_qs.author = request.user
            post_qs.save()
            return redirect('post_detail', pk=post_qs.pk)
    else:
        form = PostForm(user=request.user)
    return render(request, template, {'form': form, 'page_title': 'Новый пост'})


@permission_required('blog.change_post')
def post_edit(request, pk):
    """ Редактирование поста """

    template = 'blog/post_edit.html'
    post_qs = get_object_or_404(Post, pk=pk)

    if (request.user != post_qs.author):
        return render(request, 'blog/403.html', status=403, context={'message': "Вы не можете редактировать данную статью так как не являетесь ее автором"})

    if request.method == 'POST':
        form = PostForm(request.POST, request.user, instance=post_qs)
        if form.is_valid():
            post_qs = form.save()
            # post_qs.author = request.user
            post_qs.save()
            return redirect('post_detail', pk=post_qs.pk)
    else:
        # tags_qs = Tag.objects.filter(author=request.user)
        # tags_this_author = [tag.id for tag in tags_qs]
        form = PostForm(user=request.user, instance=post_qs)
    return render(request, template, {'form': form, 'page_title': 'Редактирование поста'})
