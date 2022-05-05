from django.contrib.admin import ModelAdmin

from dds.services.check_permission import check_permission
from dds.services.count_report import SaveCountReport
from report.models import ReportOfDate


class ReportAdmin(ModelAdmin):
    fields = ('name', 'start_date', 'end_date', 'articles', 'user')
    list_display = ('name', 'income', 'expenses', 'total')
    list_display_links = ('name',)
    readonly_fields = ('user',)
    list_filter = ('user',)
    search_fields = ('name',)
    filter_horizontal = ('articles',)

    def save_model(self, request, obj, form, change):
        SaveCountReport(
            start_date=form.cleaned_data['start_date'],
            end_date=form.cleaned_data['end_date'],
            user=request.user,
            articles=form.cleaned_data['articles'],
            obj=obj,
        ).count_and_save()

    def get_queryset(self, request):
        if check_permission(request):
            return ReportOfDate.objects.all()
        return ReportOfDate.objects.filter(user=request.user)
