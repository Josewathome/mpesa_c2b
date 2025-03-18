import requests
from django.http import JsonResponse
from datetime import datetime
from base64 import b64encode

import base64
import os
from dotenv import load_dotenv
load_dotenv()
# Get credentials from environment variables
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
MPESA_ENVIRONMENT = os.getenv('MPESA_ENVIRONMENT')
BASE_URL = "https://sandbox.safaricom.co.ke" if MPESA_ENVIRONMENT == "sandbox" else "https://api.safaricom.co.ke"

if not CONSUMER_KEY or not CONSUMER_SECRET:
    raise ValueError("Missing Mpesa API credentials. Check .env file.")

def generate_access_token():
    """Generate an OAuth access token."""
    consumer_key = CONSUMER_KEY
    consumer_secret = CONSUMER_SECRET
    url = f"{BASE_URL}/oauth/v1/generate?grant_type=client_credentials"

    # Properly encode credentials
    auth_string = f"{consumer_key}:{consumer_secret}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_auth}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        # Log error details for debugging
        print("Error generating access token:", response.json())
        response.raise_for_status()

def stk_push(request):
    """Handle STK Push."""
    access_token = generate_access_token()
    url = f"{BASE_URL}/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = b64encode(f"{os.getenv('STK_SHORTCODE')}{os.getenv('STK_PASSKEY')}{timestamp}".encode()).decode()

    payload = {
        "BusinessShortCode": os.getenv('STK_SHORTCODE'),
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": request.GET.get("amount", 1),
        "PartyA": request.GET.get("phone"),
        "PartyB": os.getenv('STK_SHORTCODE'),
        "PhoneNumber": request.GET.get("phone"),
        "CallBackURL": os.getenv('STK_CALLBACK_URL'),
        "AccountReference": "Test",
        "TransactionDesc": "STK Push Test",
    }

    response = requests.post(url, json=payload, headers=headers)
    return JsonResponse(response.json())




def b2c(request):
    """Handle B2C Payments."""
    access_token = generate_access_token()
    url = f"{BASE_URL}/mpesa/b2c/v1/paymentrequest"
    headers = {"Authorization": f"Bearer {access_token}"}

    payload = {
        "InitiatorName": os.getenv('B2C_INITIATOR_NAME'),
        "SecurityCredential": os.getenv('B2C_SECURITY_CREDENTIAL'),
        "CommandID": "PromotionPayment",
        "Amount": request.GET.get("amount", 1),
        "PartyA": os.getenv('B2C_SHORTCODE'),
        "PartyB": request.GET.get("phone"),
        "Remarks": "B2C Payment",
        "QueueTimeOutURL": os.getenv('B2C_QUEUE_TIMEOUT_URL'),
        "ResultURL": os.getenv('B2C_RESULT_URL'),
        "Occasion": "Test Occasion",
    }

    response = requests.post(url, json=payload, headers=headers)
    return JsonResponse(response.json())

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import B2CTransaction  # Ensure you have a model to store the data

@csrf_exempt
def b2c_result(request):
    """Handle B2C result notifications from Safaricom."""
    if request.method == "POST":
        try:
            # Parse the incoming JSON request body
            data = json.loads(request.body)

            # Example of parsing specific fields
            result = data.get("Result", {})
            conversation_id = result.get("ConversationID")
            originator_conversation_id = result.get("OriginatorConversationID")
            transaction_id = result.get("TransactionID")
            result_code = result.get("ResultCode")
            result_desc = result.get("ResultDesc")
            amount = None
            phone_number = None

            # Extract amount and phone number from ResultParameters, if available
            parameters = result.get("ResultParameters", {}).get("ResultParameter", [])
            for param in parameters:
                if param.get("Key") == "TransactionAmount":
                    amount = param.get("Value")
                if param.get("Key") == "PartyB":
                    phone_number = param.get("Value")

            # Save the data to the database
            B2CTransaction.objects.create(
                conversation_id=conversation_id,
                originator_conversation_id=originator_conversation_id,
                transaction_id=transaction_id,
                result_code=result_code,
                result_desc=result_desc,
                amount=amount,
                phone_number=phone_number,
                raw_response=data,  # Save the entire response for reference
            )
            print(f"The Results: {data}")
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Acknowledged Successfully"})
        except Exception as e:
            return JsonResponse({"ResultCode": 1, "ResultDesc": f"Error: {str(e)}"})
    return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid Request"})




import os
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import C2BTransaction

def c2b_register_urls(request):
    """Register C2B URLs with Safaricom."""
    access_token = generate_access_token()
    url = f"{BASE_URL}/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "ShortCode": os.getenv("C2B_SHORTCODE"),
        "ResponseType": "Completed",
        "ConfirmationURL": os.getenv("C2B_CONFIRMATION_URL"),
        "ValidationURL": os.getenv("C2B_VALIDATION_URL"),
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return JsonResponse({"status": "success", "message": response.json()})
    return JsonResponse({"status": "failure", "error": response.text})


@csrf_exempt
def dummy_validation(request):
    """Validate all transactions successfully."""
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Validation Passed"})


@csrf_exempt
def c2b_confirm(request):
    """Handle C2B confirmation notifications."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
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
                transaction_id=transaction_id,
                phone_number=phone_number,
                amount=amount,
                transaction_time=transaction_time,
                raw_response=data,
            )
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Confirmation Received"})
        except Exception as e:
            return JsonResponse({"ResultCode": 1, "ResultDesc": f"Error: {str(e)}"})
    return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid Request"})


def simulate_c2b_payment(request):
    """Simulate a C2B payment."""
    access_token = generate_access_token()
    url = f"{BASE_URL}/mpesa/c2b/v1/simulate"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "ShortCode": os.getenv("C2B_SHORTCODE"),
        "CommandID": "CustomerPayBillOnline",
        "Amount": request.GET.get("amount", 100),
        "Msisdn": request.GET.get("phone", "254722699426"),
        "BillRefNumber": request.GET.get("ref", "TestPayment"),
    }
    response = requests.post(url, json=payload, headers=headers)
    return JsonResponse(response.json())

