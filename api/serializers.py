from rest_framework import serializers
from finance.models import User, Account, Currency, Category, Transaction, Source

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')

class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="Emailingizni kiriting")

class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, help_text="Emailga kelgan 6 xonali kod")

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'name', 'code', 'rate']

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    currency_details = CurrencySerializer(source='currency', read_only=True)
    
    class Meta:
        model = Account
        fields = ['id', 'name', 'balance', 'currency', 'currency_details']

class TransactionSerializer(serializers.ModelSerializer):
    currency_code = serializers.CharField(source='currency.code', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    source_name = serializers.CharField(source='source.name', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'account', 'type', 'amount', 'currency', 
            'category', 'source', 'comment', 'date',
            'currency_code', 'category_name', 'source_name'
        ]
        read_only_fields = ['id', 'date', 'user']

    def validate(self, data):
        if data['type'] == 'expense':
            account = data['account']
            t_amount = data['amount']
            t_currency = data['currency']
            
            final_amount_for_account = (t_amount * t_currency.rate) / account.currency.rate
            
            if account.balance < final_amount_for_account:
                raise serializers.ValidationError({
                    "amount": f"Xatolik: {account.name} hamyonida mablag' yetarli emas! "
                             f"Hozirgi balans: {account.balance} {account.currency.code}. "
                             f"Siz yechmoqchi bo'lgan summa: {final_amount_for_account:.2f} {account.currency.code}."
                })
        return data