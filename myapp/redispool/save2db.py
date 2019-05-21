from django.core.management.base import BaseCommand, CommandError
from ..models import Base, Comments, Analysis


class Command(BaseCommand):
    help = 'Save 2 db'

    # 必须实现的方法
    def handle(self, *args, **options):
        for poll_id in options['poll_id']:
            try:
                poll = Base.objects.get(pk=poll_id)
            except Base.DoesNotExist:
                print('保存失败')

            poll.save()
            print('保存成功！')

            self.stdout.write('Successfully "%s"' % poll_id)