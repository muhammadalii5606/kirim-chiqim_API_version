from django.contrib import admin
from .models import User, Currency, Account, Category, Transaction, Source, EmailOTP

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'rate')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'balance', 'currency')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'account', 'type', 'amount', 'currency', 'date')
    list_filter = ('type', 'date', 'user')

admin.site.register(Source)
admin.site.register(EmailOTP)