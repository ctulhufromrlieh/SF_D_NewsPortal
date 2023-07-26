from datetime import datetime

from django.contrib.auth.models import User
from django.core.mail import mail_managers, EmailMultiAlternatives

from .models import Post, Category, PostCategory, Subscription
from .models import SchedulingMailData

def save_email_last_send_date(new_last_send_date):
    smds = SchedulingMailData.objects.all()
    if smds.count():
        smd = SchedulingMailData.objects.all()[0]
    else:
        smd = SchedulingMailData(last_send_date=new_last_send_date)

    smd.last_send_date = new_last_send_date
    smd.save()

def load_email_last_send_date():
    smds = SchedulingMailData.objects.all()
    if smds.count():
        return smds[0].last_send_date
    else:
        return None

def mass_email_sending():
    # last_send_date = get_last_send_date()
    last_send_date = load_email_last_send_date()

    sub_user_ids = Subscription.objects.all().distinct().values_list("user", flat=True)

    new_last_send_date = datetime.utcnow()

    for curr_sub_user_id in sub_user_ids:
        curr_sub_user = User.objects.get(id=curr_sub_user_id)
        curr_category_ids = Category.objects.filter(subscriptions__user=curr_sub_user).values_list("id", flat=True)

        # print(f"{curr_sub_user}'s categories: {curr_category_ids}")


        curr_posts = Post.objects.filter(categories__id__in=curr_category_ids).distinct()
        # print(f"{curr_sub_user}'s posts: {curr_posts}")

        if last_send_date:
            curr_posts = curr_posts.exclude(creation_date__lt=last_send_date)

        if curr_posts.count() == 0:
            print(f"{curr_sub_user}: Ничего нет!")

            continue

        text_content = f"Новые статьи для {curr_sub_user.username}:\n"
        html_content = f"Новые статьи для {curr_sub_user.username}:<br>"
        for curr_post in curr_posts:
            text_content += f"{curr_post.title} от {curr_post.author.user.username}: http://127.0.0.1:8000{curr_post.get_absolute_url()}\n"
            html_content += f'<a href="http://127.0.0.1:8000{curr_post.get_absolute_url()}">{curr_post.title}</a> от {curr_post.author.user.username}'

        text_contents = (text_content)
        html_contents = (html_content)

        msg = EmailMultiAlternatives(f"Новые статьи", text_contents, None, [curr_sub_user.email])
        msg.attach_alternative(html_contents, "text/html")
        msg.send()

    # save_email_last_send_date(datetime.now())
    save_email_last_send_date(new_last_send_date)

def send_email_about_post(post_id):
    instances = Post.objects.filter(id=post_id)
    if instances.count() == 0:
        return

    instance = instances[0]

    categorys = PostCategory.objects.filter(post__id=instance.id).values_list("category", flat=True)

    emails = User.objects.filter(
        subscriptions__category__in=categorys
    ).distinct().values_list('email', flat=True)

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