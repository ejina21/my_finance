import json

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect

from dds.forms import OperationForm, ReportForm
from dds.models import Operation
from dds.services.count_operation import SaveCountOperation
from dds.services.count_report import SaveCountReport
from report.models import ReportOfDate
from django.core.serializers.json import DjangoJSONEncoder

class MainView(View):
    template_name = 'main_page.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('admin/')
        user_initial = {
            'name': request.user.first_name,
            'cash': request.user.cash_sum,
        }
        return render(request, self.template_name, {'user': user_initial})


class ReportView(View):
    template_name = 'reports.html'

    def get(self, request, *args, **kwargs):
        reports = ReportOfDate.objects.filter(user=request.user).values('name', 'start_date', 'end_date', 'income', 'expenses', 'total')
        operations = Operation.objects.filter(user=request.user).values('date', 'amount', 'article__name')
        operation_json = json.dumps(list(operations), cls=DjangoJSONEncoder)
        return render(request, self.template_name, {'reports': reports, 'operations': operations, 'operations_json': operation_json})


class SendIncomeView(View):
    form_class = OperationForm
    template_name = 'create_income.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.is_purchase = False
            SaveCountOperation(
                date=form.cleaned_data['date'],
                user=request.user,
                article=form.cleaned_data['article'],
                amount=form.cleaned_data['amount'],
                obj=income,
            ).count_and_save_income()
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': form})


class SendExpensesView(View):
    form_class = OperationForm
    template_name = 'create_expenses.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            expenses = form.save(commit=False)
            expenses.is_purchase = True
            SaveCountOperation(
                date=form.cleaned_data['date'],
                user=request.user,
                article=form.cleaned_data['article'],
                amount=form.cleaned_data['amount'],
                obj=expenses,
            ).count_and_save_expenses()
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': form})


class CreateReportView(View):
    form_class = ReportForm
    template_name = 'create_report.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            SaveCountReport(
                start_date=form.cleaned_data['start_date'],
                end_date=form.cleaned_data['end_date'],
                user=request.user,
                articles=form.cleaned_data['articles'],
                obj=report,
            ).count_and_save()
            form.save_m2m()
            return HttpResponseRedirect('/report/')
        return render(request, self.template_name, {'form': form})