from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect

from dds.forms import OperationForm, ReportForm
from dds.models import Operation
from report.models import ReportOfDate


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
        reports = ReportOfDate.objects.filter(user=request.user)
        operations = Operation.objects.filter(user=request.user)
        return render(request, self.template_name, {'reports': reports, 'operations': operations})


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
            income.user = request.user
            income.is_purchase = False
            income.save()
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
            expenses.user = request.user
            expenses.is_purchase = True
            expenses.save()
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
            report.user = request.user
            report.save()
            form.save_m2m()
            return HttpResponseRedirect('/report/')
        return render(request, self.template_name, {'form': form})