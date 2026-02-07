
from .views import  WeeklyExpensesView, DailyExpensesView, MonthlyExpensesView, PaymentMethodsView, CategoryExpensesView
from django.urls import path


urlpatterns = [
    path('chart/weekly-expenses/', WeeklyExpensesView.as_view(), name='weekly-expenses'),
    path('chart/daily-expenses/', DailyExpensesView.as_view(), name='daily-expenses'),
    path('chart/monthly-expenses/', MonthlyExpensesView.as_view(), name='monthly-expenses'),
    path('chart/payment-methods-expenses/', PaymentMethodsView.as_view(), name='payment-methods-expenses'),
    path('chart/category-expenses/', CategoryExpensesView.as_view(), name='category-expenses'),
]