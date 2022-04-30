from django.db.models import Sum, Q
from dds.models import Operation
from django.contrib.admin import ModelAdmin

from dds.services.check_permission import check_permission
from report.models import ReportOfDate


class ReportAdmin(ModelAdmin):
    fields = ('name', 'start_date', 'end_date', 'articles',)
    list_display = ('name', 'income', 'expenses', 'total')
    list_display_links = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('articles',)

    def save_model(self, request, obj, form, change):
        operations = Operation.objects.values('amount').filter(
            date__gte=form.cleaned_data['start_date'],
            date__lte=form.cleaned_data['end_date'],
            user=request.user,
            article__in=form.cleaned_data['articles'],
        ).annotate(
            plus=Sum('amount', filter=Q(is_purchase=False))
        ).annotate(
            minus=Sum('amount', filter=Q(is_purchase=True))
        ).aggregate(
            income=Sum('plus'), expenses=Sum('minus'))
        obj.total = (operations.get('income') or 0) - (operations.get('expenses') or 0)
        obj.income = operations.get('income', 0) or 0
        obj.expenses = operations.get('expenses', 0) or 0
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        if check_permission(request):
            return ReportOfDate.objects.all()
        return ReportOfDate.objects.filter(user=request.user)
