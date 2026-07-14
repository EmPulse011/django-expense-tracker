import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Sum
from .models import Expense, Budget
from .forms import ExpenseForm, BudgetForm


def home(request):
    today = timezone.now().date()
    date_str = request.GET.get('date', today.isoformat())
    day_only = request.GET.get('day_only') == 'on'

    try:
        selected_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        selected_date = today
        date_str = today.isoformat()

    selected_month = selected_date.strftime("%B %Y")
    budget = Budget.objects.filter(month=selected_month).first()

    if request.method == 'POST':
        query = f"?date={date_str}" + ("&day_only=on" if day_only else "")

        if 'add_expense' in request.POST:
            form = ExpenseForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(f"/{query}")

        elif 'set_budget' in request.POST:
            budget_form = BudgetForm(request.POST, instance=budget)
            if budget_form.is_valid():
                new_budget = budget_form.save(commit=False)
                new_budget.month = selected_month
                new_budget.save()
                return redirect(f"/{query}")

    form = ExpenseForm(initial={'date': selected_date})
    budget_form = BudgetForm(instance=budget)

    month_expenses = Expense.objects.filter(
        date__month=selected_date.month,
        date__year=selected_date.year
    )
    total = sum(e.amount for e in month_expenses)
    over_budget = bool(budget and total > budget.limit)
    category_totals = (
        month_expenses.values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    expenses = month_expenses.filter(date=selected_date) if day_only else month_expenses

    context = {
        'expenses': expenses,
        'total': total,
        'budget': budget,
        'over_budget': over_budget,
        'category_totals': category_totals,
        'form': form,
        'budget_form': budget_form,
        'current_month': selected_month,
        'selected_date': date_str,
        'day_only': day_only,
    }
    return render(request, 'core/home.html', context)


def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    return redirect('home')


def delete_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    budget.delete()
    return redirect('home')


def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'core/edit_expense.html', {'form': form, 'expense': expense})