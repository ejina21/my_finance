from django.forms import ModelForm, CharField, PasswordInput, ValidationError

from dds.models import CustomUser, Operation
from report.models import ReportOfDate


class UserCreationForm(ModelForm):
    password = CharField(label='Пароль', widget=PasswordInput)
    password2 = CharField(label='Подтвердите пароль', widget=PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'cash_sum')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Пароли не совпадают')
        return cd['password2']


class OperationForm(ModelForm):
    class Meta:
        model = Operation
        fields = ('date', 'amount', 'comment', 'article')


class ReportForm(ModelForm):
    class Meta:
        model = ReportOfDate
        fields = ('name', 'start_date', 'end_date', 'articles')
