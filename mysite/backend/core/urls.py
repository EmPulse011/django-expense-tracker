from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('delete-budget/<int:pk>/', views.delete_budget, name='delete_budget'),
    path('edit/<int:pk>/', views.edit_expense, name='edit_expense'),
]