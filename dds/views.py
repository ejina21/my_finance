import json

from django.shortcuts import render
from django.views.generic import View, CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from dds.forms import OperationForm, ReportForm, UserCreationForm
from dds.models import Operation, Article
from dds.services.count_operation import SaveCountOperation
from dds.services.count_report import SaveCountReport
from report.models import ReportOfDate
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.mixins import LoginRequiredMixin


class MainView(LoginRequiredMixin, View):
    template_name = 'main_page.html'
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        user_initial = {
            'name': request.user.first_name,
            'cash': request.user.cash_sum,
        }
        return render(request, self.template_name, {'user': user_initial})


class ReportView(LoginRequiredMixin, View):
    template_name = 'reports.html'
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        reports = ReportOfDate.objects.filter(user=request.user).order_by('-end_date').values('name', 'start_date', 'end_date', 'income', 'expenses', 'total')
        operations = Operation.objects.filter(user=request.user).values('date', 'amount', 'article__name', 'is_purchase')
        operation_json = json.dumps(list(operations), cls=DjangoJSONEncoder)
        return render(request, self.template_name, {'reports': reports, 'operations': operations, 'operations_json': operation_json})


class SendIncomeView(LoginRequiredMixin, View):
    form_class = OperationForm
    template_name = 'create_income.html'
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form.fields['article'].queryset = Article.objects.filter(type_operation=Article.Type.income)
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


class SendExpensesView(LoginRequiredMixin, View):
    form_class = OperationForm
    template_name = 'create_expenses.html'
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form.fields['article'].queryset = Article.objects.filter(type_operation=Article.Type.expenses)
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


class CreateReportView(LoginRequiredMixin, View):
    form_class = ReportForm
    template_name = 'create_report.html'
    login_url = 'login'

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


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return HttpResponseRedirect(reverse('login'))
        return render(request, self.template_name, {'form': form})
