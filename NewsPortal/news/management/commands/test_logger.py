from django.core.management.base import BaseCommand, CommandError
from news.test_logger_base import check_loggers

class Command(BaseCommand):
    help = 'Тестирование логгера'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"

    def handle(self, *args, **options):
        check_loggers()