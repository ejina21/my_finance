from django.contrib import admin
from django.contrib.auth.models import Group

from report.models import ReportOfDate

admin.site.register(ReportOfDate)

admin.site.unregister(Group)