import logging
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.contrib.auth.models import User
from news.models import Post, Category, Subscription

logger = logging.getLogger(__name__)

# last_send_date = None

def get_last_send_date():
    executions = DjangoJobExecution.objects.filter(job_id="new_post_mass_notification").filter(status="Executed").order_by("-run_time").values_list("run_time", flat=True)[:1]
    if executions.count() > 0:
        return executions[0]
    else:
        return None

def new_post_mass_notification_func():
    last_send_date = get_last_send_date()

    sub_user_ids = Subscription.objects.all().distinct().values_list("user", flat=True)

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

@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            new_post_mass_notification_func,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),
            # trigger=CronTrigger(second="*/5"),  # Every 10 seconds
            id="new_post_mass_notification",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'new_post_mass_notification'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")