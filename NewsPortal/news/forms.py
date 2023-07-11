from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category, Author


class PostForm(forms.ModelForm):
    # title = forms.c

    author = forms.ModelChoiceField(queryset=Author.objects.all(), label="Автор:")
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), label="Категории:")
    title = forms.CharField(max_length=255, label="Заголовок")
    text = forms.CharField(label="Текст:")

    class Meta:
        model = Post
        fields = ['author', 'type', 'categories', 'title', 'text']


class NewForm(PostForm):
    type = forms.CharField(widget=forms.HiddenInput, initial='NEW')


class ArticleForm(PostForm):
    type = forms.CharField(widget=forms.HiddenInput, initial='ARTL')

# class NewForm(forms.ModelForm):
#
#     type = forms.CharField(widget=forms.HiddenInput, initial='NEW')
#     # title = forms.CharField(max_length=255, default="")
#
#     class Meta:
#         model = Post
#         fields = ['author', 'type', 'categories', 'title', 'text']
#
#
# class ArticleForm(forms.ModelForm):
#
#     type = forms.CharField(widget=forms.HiddenInput, initial='ARTL')
#     # title = forms.CharField(max_length=255, default="")
#
#     class Meta:
#         model = Post
#         fields = ['author', 'type', 'categories', 'title', 'text']