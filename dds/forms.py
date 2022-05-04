from django.forms import ModelForm

from dds.models import CustomUser, Operation
from report.models import ReportOfDate


class UserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'salary', 'cash_sum')


class OperationForm(ModelForm):
    class Meta:
        model = Operation
        fields = ('date', 'amount', 'comment', 'article')


class ReportForm(ModelForm):
    class Meta:
        model = ReportOfDate
        fields = ('name', 'start_date', 'end_date', 'articles')
