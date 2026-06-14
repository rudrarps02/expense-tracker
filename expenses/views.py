from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from datetime import date
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from .models import Expense
from .forms import ExpenseForm
from .serializers import ExpenseSerializer

# ==========================================
# 1. CORE DASHBOARD & INDEX VIEW
# ==========================================
def index(request):
    # Fetch all base expenses linked to the user dataset
    expenses = Expense.objects.all()

    # 1. Category filter logic query matching
    category = request.GET.get('category', '')
    if category:
        expenses = expenses.filter(category=category)

    # 2. Month filter logic query matching
    month = request.GET.get('month', '')
    if month:
        expenses = expenses.filter(date__month=month)

    # 3. Calculate total spend metric aggregation safely
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # 4. Aggregate category dataset mappings cleanly for Chart.js
    category_data = expenses.values('category').annotate(total_spent_val=Sum('amount'))
    chart_labels = [item['category'].capitalize() for item in category_data]
    chart_values = [float(item['total_spent_val']) for item in category_data]

    # 5. Core select options dropdown categories array
    categories = ['food', 'transport', 'shopping', 'bills', 'health', 'other']

    # 6. Unified context dictionary payload mapping
    context = {
        'expenses': expenses,
        'total': total,
        'categories': categories,
        'selected_category': category,
        'chart_labels': chart_labels,
        'chart_values': chart_values,
    }

    # Direct the engine output cleanly to your core index frame template
    return render(request, 'expenses/index.html', context)


# ==========================================
# 2. ADD EXPENSE TRANSACTION
# ==========================================
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ExpenseForm(initial={'date': date.today()})
    
    return render(request, 'expenses/add.html', {'form': form})


# ==========================================
# 3. DELETE EXPENSE TRANSACTION
# ==========================================
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    return redirect('index')


# ==========================================
# 4. DJANGO REST FRAMEWORK API ENDPOINTS
# ==========================================
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def expense_api_list(request):
    if request.method == 'GET':
        expenses = Expense.objects.all()
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def expense_api_list_detail(request, pk):
    try:
        expense = Expense.objects.get(pk=pk)
    except Expense.DoesNotExist:
        return Response({'error': 'Expense not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)