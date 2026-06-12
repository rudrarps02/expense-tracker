from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Expense
from .forms import ExpenseForm
from datetime import date

def index(request):
    expenses = Expense.objects.all()
    
    # Filter by category
    category = request.GET.get('category', '')
    if category:
        expenses = expenses.filter(category=category)

    # Filter by month
    month = request.GET.get('month', '')
    if month:
        expenses = expenses.filter(date__month=month)

    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'expenses': expenses,
        'total': total,
        'categories': ['food', 'transport', 'shopping', 'bills', 'health', 'other'],
        'selected_category': category,
    }
    return render(request, 'expenses/index.html', context)

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ExpenseForm(initial={'date': date.today()})
    return render(request, 'expenses/add.html', {'form': form})

def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    return redirect('index')
