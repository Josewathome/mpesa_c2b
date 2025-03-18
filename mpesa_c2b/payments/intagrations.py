# Mpesa intagrations in function and classes.

#url creation first
import requests
from django.http import JsonResponse
from datetime import datetime
from base64 import b64encode
import base64
import os
from .serializers import AccountSerializer, VerifyAccountSerializer, AccountTypeSerializer, AccountSerializer_crude, B2CTransactionserializers, STKTransactionserializers, C2BTransactionserializers
from .models import Account, AccountType, STKTransaction, C2BTransaction, B2CTransaction
from dotenv import load_dotenv
load_dotenv()
# Get credentials from environment variables
BASE_URL = os.getenv('BASE_URL')

def build_full_url(append):
    base_url = BASE_URL
    # Ensure base_url ends with '/' and append does not start with '/'
    if not base_url.endswith('/'):
        base_url += '/'
    if append.startswith('/'):
        append = append[1:]
    return f"{base_url}{append}"



# Get credentials from environment variables
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
MPESA_ENVIRONMENT = os.getenv('MPESA_ENVIRONMENT')
BASE_MPESA_URL = "https://sandbox.safaricom.co.ke" if MPESA_ENVIRONMENT == "sandbox" else "https://api.safaricom.co.ke"

if not CONSUMER_KEY or not CONSUMER_SECRET:
    raise ValueError("Missing Mpesa API credentials. Check .env file.")

def generate_access_token():
    """Generate an OAuth access token."""
    consumer_key = CONSUMER_KEY
    consumer_secret = CONSUMER_SECRET
    url = f"{BASE_MPESA_URL}/oauth/v1/generate?grant_type=client_credentials"

    # Properly encode credentials
    auth_string = f"{consumer_key}:{consumer_secret}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_auth}"
    }
    response = requests.get(url, headers=headers)
    print(response)
    if response.status_code == 200:
        try:
            return response.json().get("access_token")
        except ValueError as e:
            print(f"Error decoding JSON response: {e}")
            print("Response content:", response.text)
            raise
    else:
        # Log error details for debugging
        print("Error generating access token:", response.text)
        response.raise_for_status()
#when values not passed pass them as 0 so as to use default.
# stk_passkey, stk_shortcode
 
def STK_push(amount, phone,stk_shortcode,stk_passkey, call_backurl, business_name, business_description, TransactionType):
    """Handle STK Push."""
    access_token = generate_access_token()
    url = f"{BASE_MPESA_URL}/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    print(f'{BASE_MPESA_URL}')
    print(f"the short code in stk push {stk_shortcode}")
    print(f"the short code in stk_passkey push {stk_passkey}")
    # Determine which credentials to use
    if not stk_shortcode or not stk_passkey:
        # Fallback to environment variables if provided inputs are invalid
        print("Using environment variables for shortcode and passkey")
        stk_shortcode = os.getenv('STK_SHORTCODE')
        stk_passkey = os.getenv('STK_PASSKEY')
    else:
        print("Using provided shortcode and passkey")
    print(f"the short code used in stk push {stk_shortcode}")
    # Generate password
    password = b64encode(f"{stk_shortcode}{stk_passkey}{timestamp}".encode()).decode()
    # Create payload
    payload = {
        "BusinessShortCode": stk_shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": TransactionType,
        "Amount": amount,  # Ensure `amount` is a valid number
        "PartyA": phone,
        "PartyB": stk_shortcode,
        "PhoneNumber": phone,
        "CallBackURL": call_backurl,
        "AccountReference": business_name,
        "TransactionDesc": business_description,
    }

    # Send request
    response = requests.post(url, json=payload, headers=headers)
    
    return response

def save_STK_transaction(metadata, account_type_id):
    amount = next((item.get("Value") for item in metadata if item["Name"] == "Amount"), None)
    mpesa_receipt_number = next((item.get("Value") for item in metadata if item["Name"] == "MpesaReceiptNumber"), None)
    phone_number = next((item.get("Value") for item in metadata if item["Name"] == "PhoneNumber"), None)
    transaction_time = next((item.get("Value") for item in metadata if item["Name"] == "TransactionDate"), None)
    
    # Convert transaction_time to a datetime object
    transaction_time = datetime.strptime(str(transaction_time), "%Y%m%d%H%M%S") if transaction_time else None

    # Save transaction to the database
    STKTransaction.objects.create(
        account = account_type_id,
        transaction_id=mpesa_receipt_number,
        amount=amount,
        transaction_time=transaction_time,
        PhoneNumber=phone_number
    )
    JsonResponse({"ResultCode": 0, "ResultDesc": "Acknowledged Successfully"})
import uuid
def B2C_initiate(phone,amount,b2c_initiatorname,b2c_securitycredential,b2c_code,b2c_commandid,b2c_payment_remark,business_name, createtimeOuturl, createResulturl):
    """Handle B2C Payments."""
    access_token = generate_access_token()
    url = f"{BASE_MPESA_URL}/mpesa/b2c/v3/paymentrequest"
    headers = {"Authorization": f"Bearer {access_token}"}


    payload = {
        "OriginatorConversationID" : uuid.uuid4, # https://developer.safaricom.co.ke/APIs/BusinessToCustomer
        "InitiatorName": b2c_initiatorname,
        "SecurityCredential": b2c_securitycredential,
        "CommandID": b2c_commandid,
        "Amount": (f"{amount}", 1),
        "PartyA": b2c_code,
        "PartyB": phone, # phone number.
        "Remarks": b2c_payment_remark,
        "QueueTimeOutURL":createtimeOuturl,
        "ResultURL": createResulturl,
        "Occasion": business_name,
    }

    response = requests.post(url, json=payload, headers=headers)
    return JsonResponse(response.json())


def B2C_result(response_data, account_type_id):
    try:
        result = response_data.get("Result", {})
        
        # Extract basic details
        result_code = result.get("ResultCode")
        result_desc = result.get("ResultDesc", "No description provided")
        transaction_id = result.get("TransactionID", "N/A")
        conversation_id = result.get("ConversationID", "N/A")
        originator_conversation_id = result.get("OriginatorConversationID", "N/A")

        # Handling Success Case (ResultCode == 0)
        if result_code == 0:
            # Extract ResultParameters if available
            result_params = result.get("ResultParameters", {}).get("ResultParameter", [])
            extracted_params = {param["Key"]: param["Value"] for param in result_params if "Key" in param and "Value" in param}

            amount = extracted_params.get("TransactionAmount", "N/A")
            completed_time = extracted_params.get("TransactionCompletedDateTime", "N/A")
            receiver_name = extracted_params.get("ReceiverPartyPublicName", "N/A")

            B2CTransaction.objects.create(
                account = account_type_id,
                transaction_id=transaction_id,
                conversation_id=conversation_id,
                originator_conversation_id=originator_conversation_id,
                amount=amount,
                completed_time=completed_time,
                receiver_name=receiver_name,
                result_code=result_code,
                result_desc=result_desc,
                raw_response=response_data,  # Save the entire response for reference
            )
            
            JsonResponse({"ResultCode": 0, "ResultDesc": "Acknowledged Successfully"})

        # Handling Failure Case (ResultCode != 0)
        else:
            B2CTransaction.objects.create(
                account = account_type_id,
                transaction_id=transaction_id,
                conversation_id=conversation_id,
                originator_conversation_id=originator_conversation_id,
                result_code=result_code,
                result_desc=result_desc,
                raw_response=response_data,
            )
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Trasaction Invalid"})
             
    except Exception as e:
        return JsonResponse({"status": "Error", "message": str(e)}, status=500)














def C2B_register_urls(c2b_code, c2b_responsetype , ConfirmationURL,ValidationURL):
    """Register C2B URLs with Safaricom."""
    access_token = generate_access_token()
    url = f"{BASE_MPESA_URL}/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "ShortCode": c2b_code,
        "ResponseType": c2b_responsetype,
        "ConfirmationURL": ConfirmationURL,
        "ValidationURL": ValidationURL,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response


def C2B_confirm(data,account_type_id):
    """Handle C2B confirmation notifications."""
    try:
        transaction_id = data.get("TransID")
        phone_number = data.get("MSISDN")
        amount = data.get("TransAmount")
        transaction_time = data.get("TransTime")

        # Ensure required fields are present
        if not (transaction_id and phone_number and amount and transaction_time):
            return JsonResponse(
                {"ResultCode": 1, "ResultDesc": "Missing fields in request"}
            )

        # Save transaction to the database
        C2BTransaction.objects.create(
            account = account_type_id,
            transaction_id=transaction_id,
            phone_number=phone_number,
            amount=amount,
            transaction_time=transaction_time,
            raw_response=data,
        )
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Confirmation Received"})
    except Exception as e:
        return JsonResponse({"ResultCode": 1, "ResultDesc": f"Error: {str(e)}"})
