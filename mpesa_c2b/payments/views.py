from rest_framework import status ,generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import OrderingFilter 
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth import authenticate
from django.utils import timezone
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
import json
from datetime import datetime
from .serializers import AccountSerializer, VerifyAccountSerializer, AccountTypeSerializer,AccountSerializer_1, AccountSerializer_crude, B2CTransactionserializers, STKTransactionserializers, C2BTransactionserializers
from .models import Account, AccountType, STKTransaction, C2BTransaction, B2CTransaction
from django.contrib.auth.models import User
from .helper import Token_Auth, send_email_mail, get_Account_details
from .intagrations import build_full_url,save_STK_transaction, STK_push, B2C_initiate, B2C_result,C2B_register_urls,C2B_confirm

class SignupView(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            profile = user.profile
            profile.set_verification_code()
            user.is_active = False
            user.save()
            send_email_mail(profile.verification_code, user.email, user.username)
            
            return Response({
                'message': 'Please verify your email',
                'unique_code': str(profile.unique_code)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser) # done by @Josewathome (git) dont Touch
    def post(self, request):
        serializer = VerifyAccountSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        verification_code = serializer.validated_data['verification_code']
        unique_code = serializer.validated_data['unique_code']
        profile = get_object_or_404(Account, unique_code=unique_code)

        if profile.verification_expiry and profile.verification_expiry < timezone.now():
            profile.set_verification_code()
            send_email_mail(profile.verification_code, user.email, user.username)
            return Response({
                'error': 'Verification code expired',
                'message': 'New verification code sent to your email'
            }, status=status.HTTP_400_BAD_REQUEST)

        if profile.verification_code == verification_code:
            user = profile.user
            user.is_active = True
            user.save()
            profile.verification_code = None
            profile.verification_expiry = None
            profile.save()

            refresh, access_token = Token_Auth(unique_code, user)
            return Response({
                'message': 'Account verified successfully',
                'access_token': access_token,
                'refresh_token': str(refresh),
                'data' : get_Account_details(unique_code)
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)       

class LoginView(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')     
            auth_header = request.headers.get('Authorization')
            access_token = auth_header.split(' ')[1] if auth_header and auth_header.startswith('Bearer ') else None
            
            if username and password:
                return self.handle_password_login(username, password)

            elif access_token and username:
                return self.handle_access_token_verification(access_token, username)
                # done by @Josewathome (git) dont Touch
            return Response({'error': 'Invalid request. Please provide valid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Helper: Handle Case 1
    def handle_password_login(self, username, password):
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        profile = user.profile
        if profile.verification_code != None:
            return Response({
                'login': False,
                'message' : 'Verify Account'
            }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            refresh, access_token = Token_Auth(profile.unique_code, user)
            print(access_token)
            return Response({
                'login': True,
                'message': 'Successfully logged in',
                'access_token': access_token,
                'refresh_token': str(refresh),
                'data' : get_Account_details(profile.unique_code)
            }, status=status.HTTP_200_OK)
            
    def handle_access_token_verification(self, access_token, username):
        try:
            token = AccessToken(access_token)
            user_id = token['user_id']
            token_user = User.objects.get(id=user_id)
            if token_user.username != username:
                return Response({'error': 'Token does not match provided username'}, status=status.HTTP_401_UNAUTHORIZED)
            
            profile = token_user.profile
            if profile.verification_code != None:
                return Response({
                    'login': False,
                    'message' : 'Verify Account'
                }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                new_refresh, new_access_token = Token_Auth(profile.unique_code, token_user)
                return Response({
                    'login': True,
                    'message': 'Successfully verified token',
                    'access_token': new_access_token,
                    'refresh_token': str(new_refresh),
                    'data' : get_Account_details (profile.unique_code)
                }, status=status.HTTP_200_OK)

        except (TokenError, User.DoesNotExist) as e:
            return Response({'error': f'Access token invalid or expired: {str(e)}'}, status=status.HTTP_401_UNAUTHORIZED)

class PasswordResetView(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    def post(self, request):
        identifier = request.data.get('identifier')
        try:
            if '@' in identifier:
                user = User.objects.get(email=identifier)
            else:
                user = User.objects.get(username=identifier)

            profile = user.profile
            profile.set_verification_code()
        
            send_email_mail(profile.verification_code, user.email, user.username)
            return Response({
                'message_1': "Password successfully reset",
                'message_2': 'Verification code sent',
                'unique_code': str(profile.unique_code)
            })
        except (User.DoesNotExist, Account.DoesNotExist):
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    # password reset verification
    def patch(self, request):
        verification_code = request.data.get('verification_code')
        identifier = request.data.get('identifier')
        new_password = request.data.get('new_password')

        try:
            if '@' in identifier:
                user = User.objects.get(email=identifier)
            else:
                user = User.objects.get(username=identifier)

            profile = user.profile
            if not profile.is_verification_code_valid(verification_code):
                return Response({'error': 'Invalid or expired verification code'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            profile.verification_code = None
            profile.verification_expiry = None
            profile.save()
            
            refresh, access_token = Token_Auth(profile.unique_code, user)
            return Response({
                'message': 'Password successfully reset. Login',
                'access_token': access_token,
                'refresh_token': str(refresh),
                'data' : get_Account_details(profile.unique_code)
            }, status=status.HTTP_200_OK)
        except (User.DoesNotExist, Account.DoesNotExist):
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        username = request.data.get('username')      
        try:
            refresh = RefreshToken(refresh_token)
            user_id = refresh['user_id']
            user = User.objects.get(id=user_id, profile__isnull=False)
            if user.username != username:
                return Response({'error': 'Token does not match provided username'}, status=status.HTTP_401_UNAUTHORIZED)
            profile = user.profile
            # done by @Josewathome (git) dont Touch
            new_refresh, new_access_token = Token_Auth(profile.unique_code, user)
            refresh.blacklist()
            return Response({
                'message': 'Successfully refreshed tokens',
                'access_token': new_access_token,
                'refresh_token': str(new_refresh),
                'data' : get_Account_details(profile.unique_code)
            }, status=status.HTTP_200_OK)

        except (TokenError, User.DoesNotExist) as e:
            return Response({
                'error': 'Refresh token expired or invalid. Please login again.',
                'details': str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)
            


# Now Creating Account details of each
class AccountTypeListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer

class AccountTypeRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer
    lookup_field = 'id'
    
   #companys 
class AccountListView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountSerializer_1

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

#view all companys
class AccountListall(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountSerializer_crude
    filter_backends = [OrderingFilter]
    ordering_fields = ['unique_code']
    ordering = ['added_at']

    def get_queryset(self):
        queryset = Account.objects.all().order_by('added_at')
        top_limit = self.request.query_params.get('top', None)
        bottom_limit = self.request.query_params.get('bottom', None)

        if top_limit:
            try:
                top_limit = int(top_limit)
                return queryset[:top_limit]
            except ValueError:
                pass

        if bottom_limit:
            try:
                bottom_limit = int(bottom_limit)
                return queryset[-bottom_limit:]
            except ValueError:
                pass
        return queryset



class AccountRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountSerializer_crude
    lookup_field = 'unique_code'

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        company = serializer.save()
        user = company.user
        first_name = self.request.data.get('first_name', None)
        last_name = self.request.data.get('last_name', None)
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()

    def perform_destroy(self, instance):
        instance.delete()

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST", detail="POST method is not allowed on this endpoint")
    
    

class STKTransactionListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = STKTransactionserializers
    lookup_field = 'id'  # Define the lookup field

    def get_queryset(self):
        user = self.request.user
        transaction_id = self.kwargs.get(self.lookup_field)
        try:
            account = Account.objects.get(user=user)
        except Account.DoesNotExist:
            return STKTransaction.objects.none()  # Return an empty queryset if no account exists
        
        account_types = AccountType.objects.filter(account=account)
        queryset=  STKTransaction.objects.filter(account__in=account_types).distinct()
        if transaction_id:  # If ID is provided, filter by it
            queryset = queryset.filter(account=transaction_id)

        return queryset
 
    
class C2BTransactionListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = C2BTransactionserializers
    lookup_field = 'id'  # Define the lookup field

    def get_queryset(self):
        user = self.request.user
        transaction_id = self.kwargs.get(self.lookup_field)
        try:
            account = Account.objects.get(user=user)
        except Account.DoesNotExist:
            return C2BTransaction.objects.none()  # Return an empty queryset if no account exists
        
        account_types = AccountType.objects.filter(account=account)
        queryset=  C2BTransaction.objects.filter(account__in=account_types).distinct() 
        
        if transaction_id:  # If ID is provided, filter by it
            queryset = queryset.filter(account=transaction_id)

        return queryset
    
    
class B2CTransactionListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = B2CTransactionserializers
    lookup_field = 'id'  # Define the lookup field

    def get_queryset(self):
        user = self.request.user
        transaction_id = self.kwargs.get(self.lookup_field)  # Get 'id' from URL
        
        try:
            account = Account.objects.get(user=user)
        except Account.DoesNotExist:
            return B2CTransaction.objects.none()

        account_types = AccountType.objects.filter(account=account)
        queryset = B2CTransaction.objects.filter(account__in=account_types).distinct()

        if transaction_id:  # If ID is provided, filter by it
            queryset = queryset.filter(account=transaction_id)

        return queryset


# Mpesa Intagrations
class ProcessCallBackURLsView(View):
    def dispatch(self, request, *args, **kwargs):
        # Extract the full appended URL path after 'gen/'
        appended_url = request.path.split('gen/', 1)[-1]
        
        partsurl = appended_url.split('/')
        unique_code = partsurl[1]
        account_type_id = partsurl[2]
        value_one = partsurl[0]
        callback_data = json.loads(request.body)
        if value_one == 'stk':
            stk_callback = callback_data.get("Body", {}).get("stkCallback", {})
            
            # Process the callback data
            result_code = stk_callback.get("ResultCode")
            result_desc = stk_callback.get("ResultDesc")
            metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])
            print(result_code)
            if result_code == 0:
                response = save_STK_transaction(metadata, account_type_id)
            else:
                return JsonResponse({"ResultCode": 1, "ResultDesc": "Trasaction Invalid"})
        elif value_one == 'b2c':
            if partsurl[3] == 'tmo':
                response = {
                    "ResultCode": 0,
                    "ResultDesc": "Timeout received successfully"
                    }
            elif partsurl[3] == 're':
                response = B2C_result(callback_data, account_type_id)
                
        elif value_one == 'c2b':
            if partsurl[3] == 'val':
                """Validate all transactions successfully."""
                return JsonResponse({"ResultCode": 0, "ResultDesc": "Validation Passed"})
            elif  partsurl[3] == 'comf':
                response = C2B_confirm(callback_data, account_type_id)
            
        # Return the appended URL regardless of the HTTP method
        return JsonResponse(response, status=200)


# Stk push   
class StkPush(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            account = Account.objects.get(user=user)
        except Account.DoesNotExist:
            return Response({"error": "Account not found for the authenticated user."}, status=404)
        phone_number = request.data.get('phone_no')
        if phone_number == None: 
            phone_number = account.phone_number
            
        account_type_id = request.data.get('account_type_id')
        if account_type_id:
            try:
                account_type = account.account_types.get(id=account_type_id)
            except AccountType.DoesNotExist:
                return Response({"error": f"AccountType with ID {account_type_id} not found for this account."}, status=404)
        if not account_type:
            return Response({"error": "No account type associated with this account."}, status=404)

        stk_code = account_type.stk_code
        stk_passkey = account_type.stk_passkey
        if not stk_code:
            stk_code = 0
        if not stk_passkey:
            stk_passkey =0
        print(f"The stk code: {stk_code}")
        amount = request.data.get('amount')
        unique_code = account.unique_code
        
        createurl = f"api/gen/stk/{unique_code}/{account_type_id}"
        call_backurl = build_full_url(createurl)
        
        business_name =  account_type.business_name
        business_description = account_type.business_description
        transactiontype = account_type.transactiontype
        
        if not business_name:
            business_name = account.business
    
        response = STK_push(amount,phone_number,stk_code,stk_passkey,call_backurl,business_name,business_description, transactiontype)
        
        return JsonResponse(response.json(), status=200)
    
# B2C
class B2CPayment(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            account = Account.objects.get(user=user)
        except Account.DoesNotExist:
            return Response({"error": "Account not found for the authenticated user."}, status=404)
        phone_number = request.data.get('phone')
        account_type_id = request.data.get('account_type_id')
        if account_type_id:
            try:
                account_type = account.account_types.get(id=account_type_id)
            except AccountType.DoesNotExist:
                return Response({"error": f"AccountType with ID {account_type_id} not found for this account."}, status=404)
        if not account_type:
            return Response({"error": "No account type associated with this account."}, status=404)
        
        amount = request.data.get('amount')
        unique_code = account.unique_code
        
        createtimeOuturl = f"api/gen/b2c/{unique_code}/{account_type_id}/tmo/" # tmo = TimeOut
        createtimeOuturl = build_full_url(createtimeOuturl)
        createResulturl = f"api/gen/b2c/{unique_code}/{account_type_id}/re/" # re = result
        createResulturl = build_full_url(createResulturl)
        
        b2c_initiatorname = account_type.b2c_initiatorname
        b2c_securitycredential = account_type.b2c_securitycredential
        business_name = account_type.business_name
        if not business_name:
            business_name = account.business
        
        response = B2C_initiate(phone_number,
                       amount,
                       b2c_initiatorname,
                       b2c_securitycredential,
                       account_type.b2c_code,
                       account_type.b2c_commandid,
                       account_type.b2c_payment_remark,
                       business_name,
                       createtimeOuturl,
                       createResulturl
                       )
        return JsonResponse(response.json(), status=200)
    
# C2B transaction
class C2BPayment(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            account = Account.objects.get(user=user)
        except Account.DoesNotExist:
            return Response({"error": "Account not found for the authenticated user."}, status=404)
        account_type_id = request.data.get('account_type_id')
        if account_type_id:
            try:
                account_type = account.account_types.get(id=account_type_id)
            except AccountType.DoesNotExist:
                return Response({"error": f"AccountType with ID {account_type_id} not found for this account."}, status=404)
        if not account_type:
            return Response({"error": "No account type associated with this account."}, status=404)
        unique_code = account.unique_code
        confirmationurl = f"api/gen/c2b/{unique_code}/{account_type_id}/comf/" # comf = confirmation url
        confirmationurl = build_full_url(confirmationurl)
        validationurl = f"api/gen/c2b/{unique_code}/{account_type_id}/val/" # val = validation url
        validationurl = build_full_url(validationurl)
        c2b_code = account_type.c2b_code
        c2b_responsetype = account_type.c2b_responsetype
        response = C2B_register_urls(c2b_code, c2b_responsetype,confirmationurl,validationurl)
        
        if response.status_code == 200:
            return JsonResponse({"status": "success", "message": response.json()})
        return JsonResponse({"status": "failure", "error": response.text})
        