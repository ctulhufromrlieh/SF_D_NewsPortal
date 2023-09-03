from django.contrib import admin
from .models import Author, Category, Post, Comment, BadWord

# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    list_filter = ('user', 'rating')
    search_fields = ('user', 'rating')


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('author', 'type', 'title', 'preview_text')
    list_filter = ('author', 'type', 'creation_date')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('author', 'title', 'categories__name')  # тут всё очень похоже на фильтры из запросов в базу


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'creation_date', 'rating')
    list_filter = ('user', 'creation_date', 'rating')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('user', 'creation_date', 'rating')  # тут всё очень похоже на фильтры из запросов в базу


class BadWordAdmin(admin.ModelAdmin):
    list_display = ('text',)


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(BadWord, BadWordAdmin)
