from django.contrib.admin import ModelAdmin


class CustomUserAdmin(ModelAdmin):
    fields = ('username', 'password', 'first_name', 'last_name', 'email', 'is_superuser', 'role', 'salary', 'cash_sum')
    list_display = ('username', 'email', 'cash_sum',)
    list_display_links = ('username', 'email')
    search_fields = ('username',)
