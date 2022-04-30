from django import forms
from dds.models import CustomUser
from django.contrib.admin import ModelAdmin


class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'first_name', 'groups', 'last_name', 'is_staff', 'email', 'is_superuser', 'role', 'salary', 'cash_sum')
        widgets = {
            'password': forms.PasswordInput(),
        }


class CustomUserAdmin(ModelAdmin):
    fields = ('username', 'password', 'first_name', 'groups', 'last_name', 'is_staff', 'email', 'is_superuser', 'role', 'salary', 'cash_sum')
    list_display = ('username', 'email', 'cash_sum',)
    list_display_links = ('username', 'email')
    search_fields = ('username',)

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(form.cleaned_data['password'])
        obj.save()


