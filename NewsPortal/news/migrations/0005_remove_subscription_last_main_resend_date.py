# Generated by Django 4.2.2 on 2023-07-18 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_subscription_last_main_resend_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='last_main_resend_date',
        ),
    ]