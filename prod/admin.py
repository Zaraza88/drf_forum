from django.contrib import admin
from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)
    prepopulated_fields =  {'slug': ('title',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'category', 'slug', 
        'date_of_creation', 'is_published', 'publication_date'
    )
    list_display_links = ('title',)
    prepopulated_fields =  {'slug': ('title',)}
    search_fields = ('author', 'category', 'date_of_creation')
    list_per_page = 10
    list_filter = ('title', 'date_of_creation', 'author')
    list_editable = ('is_published',)


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'date', 'post']
    list_per_page = 10