from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect

from dds.models import Operation
from report.models import ReportOfDate


class MainView(View):
    # form_class = UserForm
    template_name = 'main_page.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('admin/')
        user_initial = {
            'name': request.user.first_name,
            'cash': request.user.cash_sum,
        }
        # form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'user': user_initial})

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         return HttpResponseRedirect('/success/')
    #
    #     return render(request, self.template_name, {'form': form})


class ReportView(View):
    template_name = 'reports.html'

    def get(self, request, *args, **kwargs):
        reports = ReportOfDate.objects.filter(user=request.user)
        operations = Operation.objects.filter(user=request.user)
        return render(request, self.template_name, {'reports': reports, 'operations': operations})
