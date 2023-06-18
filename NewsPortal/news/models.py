from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        res = 0

        posts = self.post_set.all().values("rating")
        for post in posts:
            res += 3 * post["rating"]

        from_comments = self.user.comment_set.all().values("rating")
        for from_comment in from_comments:
            res += from_comment["rating"]

        to_comments = Comment.objects.filter(post__author__pk=self.pk)
        for to_comment in to_comments:
            # print(to_comment)
            # res += to_comment["rating"]
            res += to_comment.rating

        self.rating = res
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    types = [("ARTL", "Статья"), ("NEW", "Новость")]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=4, choices=types)
    creation_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=255, default="")
    text = models.TextField(default="")
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        txt = str(self.text)
        if len(txt) > 124:
            return txt[:124] + "..."
        else:
            return txt


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default="")
    creation_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
