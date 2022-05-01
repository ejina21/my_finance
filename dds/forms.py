from django.forms import ModelForm

from dds.models import CustomUser


class UserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'salary', 'cash_sum')
