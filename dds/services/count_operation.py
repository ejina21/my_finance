import datetime

from dds.models import CustomUser, Article, Operation
from report.models import ReportOfDate


class SaveCountOperation:
    def __init__(
            self,
            date: datetime.date,
            user: CustomUser,
            article: Article,
            amount: int,
            obj: Operation,
    ):
        self.date = date
        self.user = user
        self.article = article
        self.amount = amount
        self.obj = obj
        self.queryset = self.get_queryset()

    def get_queryset(self):
        return ReportOfDate.objects.filter(
            start_date__lte=self.date,
            end_date__gte=self.date,
            user=self.user,
            articles__exact=self.article
        )

    def count_and_save_income(self):
        for report in self.queryset:
            report.total += self.amount
            report.income += self.amount
        ReportOfDate.objects.bulk_update(self.queryset, ['total', 'income'])
        self.user.cash_sum += self.amount
        self.save()

    def count_and_save_expenses(self):
        for report in self.queryset:
            report.total -= self.amount
            report.expenses += self.amount
        ReportOfDate.objects.bulk_update(self.queryset, ['total', 'expenses'])
        self.user.cash_sum -= self.amount
        self.save()

    def save(self):
        self.user.save()
        self.obj.user = self.user
        self.obj.save()
