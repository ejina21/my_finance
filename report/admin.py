from django.contrib import admin
from django.contrib.auth.models import Group

from report.admin_site.report_admin import ReportAdmin
from report.models import ReportOfDate

admin.site.register(ReportOfDate, ReportAdmin)

admin.site.unregister(Group)