from django.contrib import admin
from .models import Tag, Post

@admin.action(description="Активоровать")
def make_active(modeladmin, request, queryset):
    queryset.update(active = True)

@admin.action(description="Деактивировать")
def make_deactive(modeladmin, request, queryset):
    queryset.update(active = False)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author','updated_date', 'active')
    list_filter = ('active', 'created_date', 'updated_date', 'author')
    ordering = ['created_date']
    search_fields = ['title']
    fields = ['author', 'active', 'title', 'text', 'tags', 'created_date', 'updated_date']
    actions = [make_active, make_deactive]
    readonly_fields = ('created_date', 'updated_date')
    autocomplete_fields = ['tags']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title','author','updated_date', 'active')
    list_filter = ('active', 'created_date', 'updated_date', 'author')
    ordering = ['created_date']
    search_fields = ['title']
    fields = ['author', 'active', 'title', 'description', 'created_date', 'updated_date']
    actions = [make_active, make_deactive]
    readonly_fields = ('created_date', 'updated_date')
