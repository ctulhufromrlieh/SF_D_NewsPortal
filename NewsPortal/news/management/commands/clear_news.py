from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удалить все посты выбранной категории'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('category', nargs='+', type=str)
    def handle(self, *args, **options):
        self.stdout.readable()

        selected_category_name = options['category'][0]
        self.stdout.write(str(selected_category_name))

        # category_ids = Category.objects.filter(name__iexact=selected_category_name).values_list("id", flat=True)
        # if not category_ids.count():
        #     self.style.ERROR(f'Category <{selected_category_name}> not found!')
        #     self.stdout.write(f'Category <{selected_category_name}> not found!')
        #     return

        # selected_category_id = category_ids[0]

        # categorys = Category.objects.filter(name=selected_category_name)
        posts_to_del = Post.objects.filter(categories__name__iexact=selected_category_name)
        # posts_to_del = Post.objects.filter(categories__id__iexact=selected_category_id)
        # posts_to_del = Post.objects.filter(categories__name__icontains=selected_category_name)

        self.stdout.write(f"posts_to_del.count() = {posts_to_del.count()}")

        if not posts_to_del.count():
            self.style.ERROR(f'Category <{selected_category_name}> not found!')
            self.stdout.write(f'Category <{selected_category_name}> not found!')
            return

        # selected_category_id = categorys[0].id

        # здесь можете писать любой код, который выполнется при вызове вашей команды
        # self.stdout.readable()
        # self.stdout.write(selected_category_name)
        self.stdout.write(
            f'Do you really want to delete all post from category {selected_category_name}? yes/no')  # спрашиваем пользователя действительно ли он хочет удалить все товары
        answer = input()  # считываем подтверждение

        if answer == 'yes':  # в случае подтверждения действительно удаляем все товары
            # Post.objects.filter(category_id=).delete()
            posts_to_del.delete()

            self.stdout.write(self.style.SUCCESS('Succesfully wiped posts!'))
            return

        self.stdout.write(
            self.style.ERROR('Access denied'))  # в случае неправильного подтверждения, говорим что в доступе отказано