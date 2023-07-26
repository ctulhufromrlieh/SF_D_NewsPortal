from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import Post, Category, PostCategory
from .tasks import task_send_email_about_post


# @receiver(post_save, sender=Post)
@receiver(m2m_changed, sender=Post.categories.through)
def post_created(instance, action, **kwargs):
    if not action == "post_add":
        return

    # old-style
    # task_send_email_about_post(instance.id)

    task_send_email_about_post.delay(instance.id)


