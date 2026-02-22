from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncWeek, TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from expenses.models import Expense


def get_bom(date):
    """
    Get the beginning of the month for a given date(YYYY-MM)
    Args:  date (str): The date in the format "YYYY-MM"
    Returns:  datetime.date: The beginning of the month for the given date
    Example:  get_bom("2024-06") -> datetime.date(2024, 6, 1)
    """

    date_obj = datetime.strptime(date, "%Y-%m").date()
    beginning_of_month = date_obj.replace(day=1)
    return beginning_of_month


class WeeklyExpensesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        last_7_days = today - timedelta(days=7)

        queryset = Expense.objects.filter(user=request.user)

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if start_date:
            start_date = get_bom(start_date)
            queryset = queryset.filter(expense_date__gte=start_date)
        else:
            queryset = queryset.filter(expense_date__gte=last_7_days)

        if end_date:
            queryset = queryset.filter(expense_date__lte=end_date)

        weekly_expenses = (
            queryset.values("expense_date")
            .annotate(total=Sum("total_amount"))
            .order_by("expense_date")
        )
        date, sub_total = [], []
        total = 0
        for entry in weekly_expenses:
            if entry["expense_date"] and entry["total"] is not None:
                date.append(entry["expense_date"].strftime("%d %b"))
                sub_total.append(entry["total"])
                total += entry["total"]

        data = [{"date": date, "total": total, "sub_total": sub_total}]
        return Response(data, status=status.HTTP_200_OK)


class DailyExpensesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        queryset = Expense.objects.filter(user=request.user, expense_date=today)

        daily_expenses = queryset.values("expense_date").annotate(
            total=Sum("total_amount")
        )
        date, sub_total = [], []
        total = 0
        for entry in daily_expenses:
            if entry["expense_date"] and entry["total"] is not None:
                date.append(entry["expense_date"].strftime("%d %b"))
                sub_total.append(entry["total"])
                total += entry["total"]

        data = [{"date": date, "total": total, "sub_total": sub_total}]
        return Response(data, status=status.HTTP_200_OK)


class MonthlyExpensesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        last_12_months = today - timedelta(days=365)

        queryset = Expense.objects.filter(
            user=request.user, expense_date__gte=last_12_months
        )

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if start_date:
            start_date = get_bom(start_date)
            queryset = queryset.filter(expense_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(expense_date__lte=end_date)

        monthly_expenses = (
            queryset.annotate(month=TruncMonth("expense_date"))
            .values("month")
            .annotate(total=Sum("total_amount"))
            .order_by("month")
        )

        month, sub_total = [], []
        total = 0
        for entry in monthly_expenses:
            if entry["month"] and entry["total"] is not None:
                month.append(entry["month"].strftime("%B %Y"))
                sub_total.append(entry["total"])
                total += entry["total"]

        data = [{"month": month, "sub_total": sub_total, "total": total}]
        return Response(data, status=status.HTTP_200_OK)

    def get_month_range(self, start_date, end_date):
        months = []
        current = start_date.replace(day=1)
        while current <= end_date:
            months.append(current)
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1)
            else:
                current = current.replace(month=current.month + 1)
        return months

    def get_month_name(self, month_date):
        return month_date.strftime("%B %Y")


class PaymentMethodsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get("start_date")
        today = timezone.now().date()
        if start_date:
            today = get_bom(start_date)

        start_date = today.replace(day=1)
        queryset = Expense.objects.filter(
            user=request.user, expense_date__gte=start_date
        )

        payment_methods_expenses = (
            queryset.values("payment_method__method_name")
            .annotate(total=Sum("total_amount"))
            .order_by("payment_method__method_name")
        )

        data = []
        for entry in payment_methods_expenses:
            if entry["payment_method__method_name"] and entry["total"] is not None:
                data.append(
                    {
                        "label": entry["payment_method__method_name"],
                        "value": entry["total"],
                    }
                )

        return Response(data, status=status.HTTP_200_OK)


class CategoryExpensesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get("start_date")
        today = timezone.now().date()
        if start_date:
            today = get_bom(start_date)
        current_month = today.replace(day=1)
        queryset = Expense.objects.filter(
            user=request.user, expense_date__gte=current_month
        )

        category_expenses = (
            queryset.values("category__category_name")
            .annotate(total=Sum("total_amount"))
            .order_by("-total")
        )

        categories, sub_total = [], []
        total = 0

        for entry in category_expenses:
            if entry["category__category_name"] and entry["total"] is not None:
                categories.append(entry["category__category_name"])
                sub_total.append(entry["total"])
                total += entry["total"]
        data = [{"categories": categories, "sub_total": sub_total, "total": total}]

        return Response(data, status=status.HTTP_200_OK)
