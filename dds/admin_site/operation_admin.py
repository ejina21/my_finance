from django.contrib.admin import ModelAdmin

from report.models import ReportOfDate


class OperationAdmin(ModelAdmin):
    fields = ('date', 'amount', 'is_purchase', 'comment', 'user', 'article')
    list_display = ('date', 'amount', 'article')
    list_display_links = ('date', 'amount')
    list_filter = ('is_purchase', 'user', 'article')

    def save_model(self, request, obj, form, change):
        need_update = ReportOfDate.objects.filter(
            start_date__lte=obj.date,
            end_date__gte=obj.date,
            user=request.user,
            articles__exact=obj.article
        )
        for report in need_update:
            if obj.is_purchase:
                report.total -= obj.amount
                report.expenses += obj.amount
            else:
                report.total += obj.amount
                report.income += obj.amount
        ReportOfDate.objects.bulk_update(need_update, ['total', 'expenses', 'income'])
        obj.save()

    def has_change_permission(self, request, obj=None):
        if request.user and request.user.is_superuser:
            return True
        return False
