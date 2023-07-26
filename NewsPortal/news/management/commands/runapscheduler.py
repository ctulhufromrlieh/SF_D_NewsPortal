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

from news.email_sending import mass_email_sending

logger = logging.getLogger(__name__)

# last_send_date = None

def get_last_send_date():
    executions = DjangoJobExecution.objects.filter(job_id="new_post_mass_notification").filter(status="Executed").order_by("-run_time").values_list("run_time", flat=True)[:1]
    if executions.count() > 0:
        return executions[0]
    else:
        return None

def new_post_mass_notification_func():
    mass_email_sending()

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