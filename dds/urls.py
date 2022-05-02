from django.urls import path

from dds.views import MainView, ReportView

urlpatterns = [
    path('', MainView.as_view()),
    path('report/', ReportView.as_view()),
]
