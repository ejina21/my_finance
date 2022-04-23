from django.contrib.admin import ModelAdmin


class OperationAdmin(ModelAdmin):
    fields = ('date', 'amount', 'is_purchase', 'comment', 'user', 'article')
    list_display = ('date', 'amount', 'article')
    list_display_links = ('date', 'amount')
    list_filter = ('is_purchase', 'user', 'article')
