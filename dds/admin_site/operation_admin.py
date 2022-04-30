from dds.models import Operation
from dds.services.check_permission import check_permission
from report.models import ReportOfDate
from django.contrib.admin import ModelAdmin


class OperationAdmin(ModelAdmin):
    fields = ('date', 'amount', 'is_purchase', 'comment', 'article')
    list_display = ('date', 'amount', 'article')
    list_display_links = ('date', 'amount')
    list_filter = ('is_purchase', 'article')

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
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        if check_permission(request):
            return Operation.objects.all()
        return Operation.objects.filter(user=request.user)
