from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import Post, Category, PostCategory


# @receiver(post_save, sender=Post)
@receiver(m2m_changed, sender=Post.categories.through)
def post_created(instance, action, **kwargs):
    if not action == "post_add":
        return

    categorys = PostCategory.objects.filter(post__id=instance.id).values_list("category", flat=True)

    emails = User.objects.filter(
        subscriptions__category__in=categorys
    ).values_list('email', flat=True)

    subject = f'Вышла новая статья {instance.title} от {instance.author.user.username}!'

    text_content = (
        f'Вышел новый пост:'
        f'Автор: {instance.author.user.username}\n'
        f'Заголовок: {instance.title}\n'
        f'Превью: {instance.preview()}\n\n'        
        f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Новый пост:<br>'
        f'Автор: {instance.author.user.username}<br>'
        f'Заголовок: {instance.title}<br>'
        f'Превью: {instance.preview()}<br><br>'
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        f'Ссылка на пост</a>'
    )

    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
