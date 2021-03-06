from django.db import models

from dds.models import Article, CustomUser


class ReportOfDate(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя отчета')
    start_date = models.DateField(verbose_name='Дата начала периода')
    end_date = models.DateField(verbose_name='Дата окончания периода')
    total = models.IntegerField(verbose_name='Итого по периоду', default=0)
    income = models.PositiveIntegerField(verbose_name='Доходы по периоду', default=0)
    expenses = models.PositiveIntegerField(verbose_name='Расходы по периоду', default=0)
    articles = models.ManyToManyField(
        Article,
        verbose_name='Статьи для рассчета',
        related_name='report',
        help_text='Оставить пустым, если нужно посчитать для всех статей',
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='report')

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'

    def __str__(self):
        return self.name
