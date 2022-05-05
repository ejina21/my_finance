from dds.models import Operation
from dds.services.check_permission import check_permission
from dds.services.count_operation import SaveCountOperation
from report.models import ReportOfDate
from django.contrib.admin import ModelAdmin


class OperationAdmin(ModelAdmin):
    fields = ('date', 'amount', 'is_purchase', 'comment', 'article', 'user')
    list_display = ('date', 'amount', 'article')
    readonly_fields = ('user',)
    list_display_links = ('date', 'amount')
    list_filter = ('is_purchase', 'article', 'user')

    def save_model(self, request, obj, form, change):
        count = SaveCountOperation(
            date=form.cleaned_data['date'],
            user=request.user,
            article=form.cleaned_data['article'],
            amount=form.cleaned_data['amount'],
            obj=obj,
        )
        count.count_and_save_expenses() if form.cleaned_data['is_purchase'] else count.count_and_save_income()

    def get_queryset(self, request):
        if check_permission(request):
            return Operation.objects.all()
        return Operation.objects.filter(user=request.user)
