from django.forms import ModelForm, CharField, PasswordInput, ValidationError, DateInput
from dds.models import CustomUser, Operation
from report.models import ReportOfDate


class UserCreationForm(ModelForm):
    password = CharField(label='Пароль', widget=PasswordInput)
    password2 = CharField(label='Подтвердите пароль', widget=PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'cash_sum')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Пароли не совпадают')
        return cd['password2']


class OperationFormExpenses(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OperationFormExpenses, self).__init__(*args, **kwargs)
        self.fields['article'].label = "Статья расхода"

    class Meta:
        model = Operation
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }
        fields = ('date', 'amount', 'comment', 'article')


class OperationFormIncome(OperationFormExpenses):
    def __init__(self, *args, **kwargs):
        super(OperationFormExpenses, self).__init__(*args, **kwargs)
        self.fields['article'].label = "Статья дохода"


class ReportForm(ModelForm):
    class Meta:
        model = ReportOfDate
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }
        fields = ('name', 'start_date', 'end_date', 'articles')
