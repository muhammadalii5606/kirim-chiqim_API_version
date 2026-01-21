import random
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal

from finance.models import User, EmailOTP, Account, Currency, Transaction, Category, Source
from .serializers import (
    SendOTPSerializer, VerifyOTPSerializer, UserSerializer, 
    AccountSerializer, TransactionSerializer, CategorySerializer, SourceSerializer
)

class SendOTPView(APIView):
    serializer_class = SendOTPSerializer
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = str(random.randint(100000, 999999))
            EmailOTP.objects.update_or_create(email=email, defaults={'otp': otp_code, 'created_at': timezone.now()})
            request.session['user_email'] = email
            request.session.modified = True
            send_mail('Tasdiqlash kodi', f'Kodingiz: {otp_code}', settings.EMAIL_HOST_USER, [email])
            return Response({"message": "OTP yuborildi"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    serializer_class = VerifyOTPSerializer
    def post(self, request):
        otp = request.data.get('otp')
        email = request.session.get('user_email')
        if not email:
            last_otp = EmailOTP.objects.filter(otp=otp).order_by('-created_at').first()
            if last_otp: email = last_otp.email
        if not email: return Response({"error": "Email topilmadi"}, status=status.HTTP_400_BAD_REQUEST)
        otp_obj = EmailOTP.objects.filter(email=email, otp=otp).first()
        if otp_obj and otp_obj.is_valid():
            user, _ = User.objects.get_or_create(email=email)
            refresh = RefreshToken.for_user(user)
            otp_obj.delete()
            return Response({"access": str(refresh.access_token), "refresh": str(refresh), "user": UserSerializer(user).data})
        return Response({"error": "Kod xato"}, status=status.HTTP_400_BAD_REQUEST)

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        total_uzs = sum(acc.balance * acc.currency.rate for acc in accounts)
        recent_transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:10]
        return Response({"total_balance_uzs": total_uzs, "accounts": AccountSerializer(accounts, many=True).data, "recent_transactions": TransactionSerializer(recent_transactions, many=True).data})

class AccountListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer
    def get_queryset(self): return Account.objects.filter(user=self.request.user)

class TransactionCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    def perform_create(self, serializer):
        with transaction.atomic():
            account = serializer.validated_data['account']
            t_type = serializer.validated_data['type']
            t_amount = Decimal(str(serializer.validated_data['amount']))
            t_currency = serializer.validated_data['currency']
            converted_amount = (t_amount * t_currency.rate) / account.currency.rate if t_currency != account.currency else t_amount

            if t_type == 'expense':
                if account.balance < converted_amount:
                    raise ValidationError({"error": f"Mablag' yetarli emas! Balans: {account.balance}"})
                account.balance -= converted_amount
            else:
                account.balance += converted_amount
            
            account.save()
            serializer.save(user=self.request.user)

class CategoryListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer