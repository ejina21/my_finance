from django.shortcuts import render

from django.views.generic import View
from django.http import HttpResponseRedirect

from dds.forms import UserForm


class MainView(View):
    form_class = UserForm
    template_name = 'test.html'

    def get(self, request, *args, **kwargs):
        user_initial = {
            'name': request.user.first_name,
            'cash': request.user.cash_sum,
        }
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form, 'user': user_initial})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})