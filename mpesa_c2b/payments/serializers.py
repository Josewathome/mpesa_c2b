
# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account,AccountType,B2CTransaction,C2BTransaction,STKTransaction

class AccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'phone_number' ]
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=password
        )
        
        profile = Account.objects.create(user=user, **validated_data)
        return user
    
class VerifyAccountSerializer(serializers.Serializer):
    verification_code = serializers.CharField(required=True)
    unique_code = serializers.UUIDField(required=True)
  
class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = '__all__'
    
class UserSerializer_1(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')  # Exclude password
    
class AccountSerializer_1(serializers.ModelSerializer):
    user = UserSerializer_1()  # Simplify user representation
    #subscriptions = SubscriptionSerializer_1(many=True) # done by @Josewathome (git) dont Touch
    account_types = AccountTypeSerializer(many=True)
    class Meta:
        model = Account
        exclude = ('added_at', 'updated_at')
        
class UserSerializer_crude(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name','last_name']
        read_only_fields = ['username', 'email']  # Prevent modification
        
class AccountSerializer_crude(serializers.ModelSerializer):
    user = UserSerializer_crude(read_only=True)
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ['unique_code'] 
        
        
class B2CTransactionserializers(serializers.ModelSerializer):
    class Meta:
        model = B2CTransaction
        fields = '__all__'
class STKTransactionserializers(serializers.ModelSerializer):
    class Meta:
        model = STKTransaction
        fields = '__all__'
class C2BTransactionserializers(serializers.ModelSerializer):
    class Meta:
        model = C2BTransaction
        fields = '__all__'