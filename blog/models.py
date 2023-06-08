from django.conf import settings
from django.db import models

class Tag(models.Model):
    """ Tags of posts """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание тега', null=True, blank=True)

    created_date = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_date = models.DateTimeField('Дата изменения', auto_now=True)
    active = models.BooleanField('Активно', default=False)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title

class Post(models.Model):
    """ Post of blog """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    title = models.CharField('Название', max_length=200)
    text = models.TextField('Содержание')
    created_date = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_date = models.DateTimeField('Дата изменения', auto_now=True)
    active = models.BooleanField('Активно', default=False)
    tags = models.ManyToManyField(Tag)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title
