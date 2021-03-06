from django.urls import path

from dds.views import MainView, ReportView, SendIncomeView, SendExpensesView, CreateReportView, ReportDetailView

urlpatterns = [
    path('', MainView.as_view(), name='site'),
    path('report/', ReportView.as_view()),
    path('report/<int:pk>/', ReportDetailView.as_view(), name='del_report'),
    path('send-income/', SendIncomeView.as_view()),
    path('send-expenses/', SendExpensesView.as_view()),
    path('create-report/', CreateReportView.as_view()),
]
