from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_expense, name='add_expense'),
    path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_expense, name='add_expense'),
    path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),
    # API Link
    path('api/expenses/', views.expense_api_list, name='expense_api_list'),
]