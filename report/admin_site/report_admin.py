from django.contrib.admin import ModelAdmin


class ReportAdmin(ModelAdmin):
    fields = ('name', 'start_date', 'end_date', 'articles', 'user',)
    list_display = ('name', 'income', 'expenses', 'total')
    list_display_links = ('name',)
    list_filter = ('user',)
    search_fields = ('name',)
    filter_horizontal = ('articles',)
