from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('send-otp/', views.SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify-otp'),
    
    # Dashboard & Data
    path('dashboard/', views.DashboardAPIView.as_view(), name='dashboard'),
    path('accounts/', views.AccountListView.as_view(), name='account-list'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    
    # Transactions
    path('transactions/create/', views.TransactionCreateView.as_view(), name='transaction-create'),
]