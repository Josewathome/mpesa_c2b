from django.db import models
import uuid
from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone

# Account Model to store user-specific accounts
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    unique_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    account_name = models.CharField(max_length=255)
    business = models.CharField(max_length=255, blank=True, help_text= "This Is the name of the business")
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    verification_expiry = models.DateTimeField(null=True, blank=True)
    
    is_user = models.BooleanField(default=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def set_verification_code(self):
        # Generate a 6-digit code
        self.verification_code = "{:06d}".format(uuid.uuid4().int % 1000000)
        self.verification_expiry = timezone.now() + timedelta(minutes=20) #20 minutes
        self.save()

    def is_verification_code_valid(self, code):
        code_1 = str(code).strip()
        # Check if code matches and is still valid
        stored_code = str(self.verification_code).strip()
        return (
            stored_code == code_1 and
            timezone.now() < self.verification_expiry
        )
        
    def __str__(self):
        return f"{self.unique_code} - {self.user.username} - {self.id}"




# AccountType Model to store various account types associated with a user's account
class AccountType(models.Model):
    choices = {
        ('CustomerPayBillOnline' , ('CustomerPayBillOnline')),
        ('CustomerBuyGoodsOnline', ('CustomerBuyGoodsOnline'))
    }
    choices_b2c =  {
        ('PromotionPayment' , ('PromotionPayment')),
        ('BusinessPayment', ('BusinessPayment')),
        ('SalaryPayment', ('SalaryPayment')),
    }
    choices_types = {
        ('Completed', ('Completed')),
        ('Cancelled',('Cancelled'))
    }
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account_types")
    business_name = models.CharField(max_length=255, blank=True,null=True, help_text= "This Is the name of the business")
    business_description = models.CharField(max_length=255, null=True, blank=True, default="STK Push")
    
    stk_code = models.CharField(max_length=255, null=True, blank=True)
    stk_passkey = models.TextField(null=True, blank=True)
    transactiontype = models.CharField(max_length=225,choices=choices, default="CustomerPayBillOnline")
    
    b2c_initiatorname = models.CharField(max_length=255, null=True, blank=True, help_text='your user name')
    b2c_securitycredential = models.CharField(max_length=255, null=True, blank=True)
    b2c_code = models.CharField(max_length=255, null=True, blank=True)
    b2c_commandid = models.CharField(choices=choices_b2c, default='BusinessPayment', max_length=255)
    b2c_payment_remark = models.CharField(max_length=255, null=True, blank=True, default="Payment Ok")
    # b2c occation will be business name.
    
    c2b_code = models.CharField(max_length=255, null=True, blank=True)
    c2b_responsetype = models.CharField(max_length=225,choices=choices_types, default="Completed")
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.business_name} - {self.account.account_name} - {self.id}"

# STKTransaction Model to store transactions for a particular account type
class STKTransaction(models.Model):
    account = models.ManyToManyField(AccountType, related_name="stk_transactions")
    transaction_id = models.CharField(max_length=100, unique=True, db_index=True) # MpesaReceiptNumber
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_time = models.DateTimeField()
    PhoneNumber = models.IntegerField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.amount}"

# C2BTransaction Model to store C2B transactions
class C2BTransaction(models.Model):
    account = models.ManyToManyField(AccountType, related_name="c2b_transactions")
    transaction_id = models.CharField(max_length=100, unique=True, db_index=True)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_time = models.DateTimeField()
    raw_response = models.JSONField()
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.phone_number} - {self.amount}"

# B2CTransaction Model to store B2C transactions
class B2CTransaction(models.Model):
    account = models.ManyToManyField(AccountType, related_name="b2c_transactions")
    conversation_id = models.CharField(max_length=100, unique=True, db_index=True)
    originator_conversation_id = models.CharField(max_length=100)
    transaction_id =  models.CharField(max_length=255, null=True, blank=True)
    result_code =  models.CharField(max_length=255, null=True, blank=True)
    result_desc =  models.CharField(max_length=255, null=True, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    receiver_name =  models.CharField(max_length=255, null=True, blank=True)
    completed_time = models.CharField(max_length=100,null=True, blank=True)
    charges =  models.CharField(max_length=255, null=True, blank=True)
    currency = models.CharField(max_length=255, null=True, blank=True)
    raw_response = models.JSONField()
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.transaction_id} - {self.amount}"
