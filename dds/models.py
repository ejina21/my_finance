from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Администратор'
        USER = 'user', 'Пользователь'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER, verbose_name='Роль')
    salary = models.PositiveIntegerField(verbose_name='Зарплата', default=0)
    cash_sum = models.IntegerField(verbose_name='Средств в наличии', default=0)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Operation(models.Model):
    date = models.DateField(verbose_name='Дата операции')
    amount = models.IntegerField(verbose_name='Сумма')
    is_purchase = models.BooleanField(default=True, verbose_name='Является расходом')
    comment = models.CharField(max_length=200, blank=True, verbose_name='Комментарий')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='operation')
    article = models.ForeignKey('Article', on_delete=models.CASCADE, verbose_name='Статья дохода/расхода', related_name='operation')

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Финансовая операция'
        verbose_name_plural = 'Финансовые операции'

    def __str__(self):
        return f'{self.amount}_{self.article}'


class Article(models.Model):
    class Type(models.TextChoices):
        income = 'income', 'Доход'
        expenses = 'expenses', 'Расход'

    type_operation = models.CharField(max_length=10, choices=Type.choices, verbose_name='Тип операции')
    name = models.CharField(max_length=100, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Статья доходов/расходов'
        verbose_name_plural = 'Статьи доходов/расходов'
        unique_together = ('type_operation', 'name')

    def __str__(self):
        return f'{self.get_type_operation_display()}_{self.name}'
