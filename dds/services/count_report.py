import datetime
from django.db.models import Sum, Q

from dds.models import CustomUser, Article, Operation
from report.models import ReportOfDate


class SaveCountReport:
    def __init__(
            self,
            start_date: datetime.date,
            end_date: datetime.date,
            user: CustomUser,
            articles: list[Article],
            obj: ReportOfDate,
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.user = user
        self.articles = articles
        self.obj = obj

    def count_and_save(self):
        operations = Operation.objects.values('amount').filter(
            date__gte=self.start_date,
            date__lte=self.end_date,
            user=self.user,
            article__in=self.articles,
        ).annotate(
            plus=Sum('amount', filter=Q(is_purchase=False))
        ).annotate(
            minus=Sum('amount', filter=Q(is_purchase=True))
        ).aggregate(
            income=Sum('plus'), expenses=Sum('minus'))
        self.obj.total = (operations.get('income') or 0) - (operations.get('expenses') or 0)
        self.obj.income = operations.get('income', 0) or 0
        self.obj.expenses = operations.get('expenses', 0) or 0
        self.obj.user = self.user
        self.obj.save()
