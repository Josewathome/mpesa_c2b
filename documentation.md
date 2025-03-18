### base url : http://127.0.0.1:8000/
base url to be stored in a .env file
```markdown
### 1. singup methods:
url: /api/signup/
method: POST
header: None
input
```json
{
    "username" :"qqqqqlxsxq",
    "password" : "1q2w3el4r5txx6y7u8iqs9o0p-[",
    "email": "qq@ai.com",

}
```
output
```json
 {
    "message": "Please verify your email",
    "unique_code": "8f7563c5-9399-4208-81af-80cd3f05238d"
}
```
---

### 2. Verify Account
url: /api/verify-email/
method: POST
header: None
input:
```json
{
	"unique_code": "b0bec13d-cb5d-47bd-bbdf-f0615c29e122",
    "verification_code" : 940346

}
```
output
```json
{
    "message": "Account verified successfully",
    "access_token": "eyJhbG9pZCItD..........17974UEOc-_OhSis",
    "refresh_token": "eyJhbGciCIsIn.......lDSfPTp3cn-Ong",
    "data": {
        "id": 10,
        "user": {
            "id": 11,
            "username": "oo",
            "first_name": "",
            "last_name": ""
        },
        "account_types": [],
        "unique_code": "b0bec13d-cb5d-47bd-bbdf-f0615c29e122",
        "account_name": "x",
        "business": "",
        "phone_number": null,
        "location": null,
        "verification_code": null,
        "verification_expiry": null,
        "is_user": true
    }
}
```
---

### 3. Login
Login using username and password
url: /api/login/
method: POST
header: None
input:
```json
{
    "username" :"oo",
    "password" : "1q2wx3el4r5ctxx6y7u8iqs9o0p-["
}
```
output
```json
{
    "login": true,
    "message": "Successfully logged in",
    "access_token": "eyJhbl9.......6Zj8UEJMIo",
    "refresh_token": "eyJh...........xOqbQRdLk",
    "data": {
        "id": 10,
        "user": {
            "id": 11,
            "username": "oo",
            "first_name": "",
            "last_name": ""
        },
        "account_types": [],
        "unique_code": "b0bec13d-cb5d-47bd-bbdf-f0615c29e122",
        "account_name": "x",
        "business": "",
        "phone_number": null,
        "location": null,
        "verification_code": null,
        "verification_expiry": null,
        "is_user": true
    }
}
```
---

#### . Login 2
Login using username and Access token
url: /api/login/
method: POST
header: Bearer Token (Access token)
input:
```json
{
    "username" :"oo"
   
}
```
output
```json
{
    "login": true,
    "message": "Successfully verified token",
    "access_token": "eyJ........._pSZ6M",
    "refresh_token": "ey..........laqE",
    "data": {
        "id": 10,
        "user": {
            "id": 11,
            "username": "oo",
            "first_name": "",
            "last_name": ""
        },
        "account_types": [],
        "unique_code": "b0bec13d-cb5d-47bd-bbdf-f0615c29e122",
        "account_name": "x",
        "business": "",
        "phone_number": null,
        "location": null,
        "verification_code": null,
        "verification_expiry": null,
        "is_user": true
    }
}
```

### If you get this response then Means account not yet verified or password change
**unauthorized 401 response***:
```json
{
    "login": false,
    "message": "Verify Account"
}
```
---

### 4. Password Reset
url: /api/password-reset/
method: POST
header: None
input:
```json
{
    "identifier" :"oo" // can be username or Email
}
```
output
```json
{
    "message_1": "Password successfully reset",
    "message_2": "Verification code sent",
    "unique_code": "b0bec13d-cb5d-47bd-bbdf-f0615c29e122"
}

```
---

### 5. Password Reset
url: /api/password-reset/
method: PATCH
header: None
input:
```json
{
    "identifier" :"oo", // can be username or Email
	"verification_code" : 250926,
	"new_password" : "YHE56673"
}
```
output
```json
{
    "message": "Password successfully reset. Login",
    "access_token": "ey......lXY4",
    "refresh_token": "eyJ..........tEA4",
    "data": {
        "id": 10,
        "user": {
            "id": 11,
            "username": "oo",
            "first_name": "",
            "last_name": ""
        },
        "account_types": [],
        "unique_code": "b0bec13d-cb5d-47bd-bbdf-f0615c29e122",
        "account_name": "x",
        "business": "",
        "phone_number": null,
        "location": null,
        "verification_code": null,
        "verification_expiry": null,
        "is_user": true
    }
}

```
---
### 6. Refresh Token Update
this is to get a new Token
url: /api/refresh-token/
method: POST
header: None
input:
```json
{
    "username" :"oo",
    "refresh_token": "eyJhbGci....._tEA4"
}
```
output
```json
{
    "message": "Successfully refreshed tokens",
    "access_token": "eyJhbG....4ERDM4",
    "refresh_token": "eyJ......A39Uiac",
    "data": {
        "id": 10,
        "user": {
            "id": 11,
            "username": "oo",
            "first_name": "",
            "last_name": ""
        },
        "account_types": [],
        "unique_code": "b0bec13d-cb5d-47bd-bbdf-f0615c29e122",
        "account_name": "x",
        "business": "",
        "phone_number": null,
        "location": null,
        "verification_code": null,
        "verification_expiry": null,
        "is_user": true
    }
}
```
---


### 7. listing all Accounts for the user:

Top 10 results: GET /api/accountall/?top=10
Bottom 20 results: GET /api/accountall/?bottom=20
All results: GET /api/accountall/
```json
[
    {
        "id": 8,
        "user": {
            "id": 9,
            "username": "qqqqqlxsxcq",
            "email": "qq@ai.com",
            "first_name": "",
            "last_name": ""
        },
        "unique_code": "c4a29454-a5a3-4df7-a258-68c36cf54063",
        "account_name": "",
        "business": "",
        "phone_number": null,
        "location": null,
        "verification_code": "984886",
        "verification_expiry": "2025-01-22T19:53:21.647136Z",
        "is_user": true,
        "added_at": "2025-01-22T19:33:21.636183Z",
        "updated_at": "2025-01-22T19:33:21.647342Z"
    },
    {
        "id": 9,
        "user": {
            "id": 10,
            "username": "qqqqxqlxsxcq",
            "email": "qq@ai.com",
            "first_name": "",
            "last_name": ""
        },
        "unique_code": "17d72892-779a-4c3d-b18a-4ac46c60520c",
        "account_name": "",
        "business": "",
        "phone_number": null,
        "location": null,
        "verification_code": "384069",
        "verification_expiry": "2025-01-22T19:53:47.637638Z",
        "is_user": true,
        "added_at": "2025-01-22T19:33:47.629361Z",
        "updated_at": "2025-01-22T19:33:47.637837Z"
    },
    {
        "id": 10,
        "user": {
            "id": 11,
            "username": "oo",
            "email": "qq@ai.com",
            "first_name": "",
            "last_name": ""
        },
        "unique_code": "b0bec13d-cb5d-47bd-bbdf-f0615c29e122",
        "account_name": "x",
        "business": "",
        "phone_number": null,
        "location": null,
        "verification_code": null,
        "verification_expiry": null,
        "is_user": true,
        "added_at": "2025-01-22T19:35:00.173723Z",
        "updated_at": "2025-01-22T20:02:07.637277Z"
    }
]
```
---

### 8. Getting account for a user
This getss account for the verified user of the token
url: /api/account/
method: Get
header: Bearer Token (Access token)
input: None

**Output** :
```json
[
    {
        "id": 10,
        "user": {
            "id": 12,
            "username": "qqqqqlxsxq",
            "first_name": "",
            "last_name": ""
        },
        "account_types": [
            {
                "id": 1,
                "business_name": null,
                "business_description": "STK Push",
                "stk_code": null,
                "stk_passkey": "",
                "transactiontype": "CustomerPayBillOnline",
                "b2c_initiatorname": null,
                "b2c_securitycredential": "initiator_name",
                "b2c_code": "B2C123",
                "b2c_commandid": "BusinessPayToBulk",
                "b2c_payment_remark": "Payment Ok",
                "c2b_code": "C2B456",
                "c2b_responsetype": "Completed",
                "added_at": "2025-01-22T20:35:58.864190Z",
                "updated_at": "2025-01-25T09:31:17.844067Z",
                "account": 10
            }
        ],
        "unique_code": "b8cb53fc-e491-4018-b307-89e4b60c6385",
        "account_name": "saf",
        "business": "",
        "phone_number": null,
        "location": null,
        "verification_code": null,
        "verification_expiry": null,
        "is_user": true
    }
]
```
---

### 9. Modify and update Account.
url: /api/account/<str:unique_code>/
method: PATCH,DELETE
header:
input:
```json
{
	"first_name": "",
	"last_name": "DDDDDDDDDDDDD"
	"account_name": "x",
	"business": "",
	"phone_number": null,
	"location": null,
}

```
output
```json
{
    "id": 10,
    "user": {
        "id": 11,
        "username": "oo",
        "email": "qq@ai.com",
        "first_name": "",
        "last_name": "DDDDDDDDDDDDDDD"
    },
    "unique_code": "b0bec13d-cb5d-47bd-bbdf-f0615c29e122",
    "account_name": "x",
    "business": "",
    "phone_number": null,
    "location": null,
    "verification_code": null,
    "verification_expiry": null,
    "is_user": true,
    "added_at": "2025-01-22T19:35:00.173723Z",
    "updated_at": "2025-01-22T20:17:16.720974Z"
}
```
---
for delliting you get this output.
method: DELETE
Output: no response


# Account Type API

This API provides endpoints to manage account types associated with user accounts. The `AccountType` model is used to store various account types and their details.

## Endpoints

### 10. List and Create Account Types
Always Go here get your consumer key and secrete: https://developer.safaricom.co.ke/GoLive
**URL**: `/api/account-type/`  
**Method**: `GET`, `POST`  
**View**: `AccountTypeListCreateView`
**header**: Bearer Token (Access token)
#### Input
##### For `GET`:
No input required.

##### For `POST`:
```json
{
    "account": <account_id>,
    "name": "Savings Account",
    "stk_code": "STK123",
    "b2c_initiator": "initiator_name",
    "b2c_security": "security_key",
    "b2c_code": "B2C123",
    "c2b_code": "C2B456"
}
```

#### Output
##### For `GET`:
Returns a list of all account types:
```json
[
    {
        "id": 1,
        "account": 1,
        "name": "Savings Account",
        "stk_code": "STK123",
        "b2c_initiator": "initiator_name",
        "b2c_security": "security_key",
        "b2c_code": "B2C123",
        "c2b_code": "C2B456",
        "added_at": "2025-01-20T12:00:00Z",
        "updated_at": "2025-01-21T15:00:00Z"
    }
]
```

##### For `POST`:
Returns the created account type:
```json
{
    "id": 2,
    "account": 1,
    "name": "Current Account",
    "stk_code": "STK456",
    "b2c_initiator": "new_initiator",
    "b2c_security": "new_security",
    "b2c_code": "B2C789",
    "c2b_code": "C2B987",
    "added_at": "2025-01-22T10:00:00Z",
    "updated_at": "2025-01-22T10:00:00Z"
}
```

---

### 11. Retrieve, Update, or Delete an Account Type
**URL**: `/api/account-typeupdate/<int:id>/`  
**Method**: `GET`, `PATCH`, `DELETE`  
**View**: `AccountTypeRetrieveUpdateDeleteView`
**header**: Bearer Token (Access token)
#### Input
##### For `GET`:
- **Parameter**: `id` - The ID of the account type to retrieve.

##### For `PATCH`:
```json
{
    "name": "Updated Account Name"
}
```

##### For `DELETE`:
- **Parameter**: `id` - The ID of the account type to delete.

#### Output
##### For `GET`:
Returns the details of the specified account type:
```json
{
    "id": 1,
    "account": 1,
    "name": "Savings Account",
    "stk_code": "STK123",
    "b2c_initiator": "initiator_name",
    "b2c_security": "security_key",
    "b2c_code": "B2C123",
    "c2b_code": "C2B456",
    "added_at": "2025-01-20T12:00:00Z",
    "updated_at": "2025-01-21T15:00:00Z"
}
```

##### For `PATCH`:
Returns the updated account type:
```json
{
    "id": 1,
    "account": 1,
    "name": "Updated Account Name",
    "stk_code": "STK123",
    "b2c_initiator": "initiator_name",
    "b2c_security": "security_key",
    "b2c_code": "B2C123",
    "c2b_code": "C2B456",
    "added_at": "2025-01-20T12:00:00Z",
    "updated_at": "2025-01-22T10:30:00Z"
}
```

##### For `DELETE`:
Returns a success message:
```json
{
    "message": "Account type deleted successfully."
}
```

---

## Authentication
These endpoints use `JWTAuthentication`. Ensure a valid JWT token is included in the `Authorization` header as a Bearer token.

---

## Models

### AccountType Model
The `AccountType` model is used to store various account types associated with a user's account. Below is the structure:

| Field           | Type           | Description                                   |
|------------------|----------------|-----------------------------------------------|
| `account`        | ForeignKey     | Links to the `Account` model.                |
| `name`           | CharField      | Name of the account type.                    |
| `stk_code`       | CharField      | Short code for the account type.             |
| `b2c_initiator`  | CharField      | B2C initiator name.                          |
| `b2c_security`   | CharField      | Security key for B2C transactions.           |
| `b2c_code`       | CharField      | Code for B2C transactions.                   |
| `c2b_code`       | CharField      | Code for C2B transactions.                   |
| `added_at`       | DateTimeField  | Timestamp when the account type was created. |
| `updated_at`     | DateTimeField  | Timestamp when the account type was updated. |

---
# 12 Access token invalid or expired.
**Response**:
```json
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalid or expired"
        }
    ]
}
```
---

# 13. Now Using The APIs to now use Mpesa.
### 1. STK
**url**: /api/stk/
**method**: POST
**header**: Bearer Token (Access token)
**input**:
```json
{
    "account_type_id" : 1,
    "amount" : 1,
    "phone_no" : 254722699426
}

```
**Output**:
```json

```
---

### 2. B2C payment
eg sararly, business, promotional payments
**url**: /api/b2c/
**method**: POST
**header**: Bearer Token (Access token)
**input**:
```json
{
    "account_type_id" : 1,
    "amount" : 1,
    "phone" : 254722699426
}

```
**Output**:
```json

```
---

### 3. C2B payment
**url**: /api/c2b/
**method**: POST
**header**: Bearer Token (Access token)
**input**:
```json
{
    "account_type_id" : 1,
    "amount" : 1,
    "phone" : 254722699426
}

```
**Output**:
```json

```
---



BASE URL: https://2e36-102-209-137-62.ngrok-free.app
### 1. STK Data.
**url**: /api/stk-transactions/
**method**: GET
**header**: Bearer Token (Access token)
```
**Output**:
```json
[
    {
        "id": 1,
        "transaction_id": "1212321414123421",
        "amount": "253.00",
        "transaction_time": "2025-02-17T06:00:00Z",
        "PhoneNumber": 725864895,
        "added_at": "2025-02-17T09:34:14.346750Z",
        "updated_at": "2025-02-17T09:34:14.346800Z",
        "account": [
            2
        ]
    },
    {
        "id": 2,
        "transaction_id": "124325frdr346r",
        "amount": "256.23",
        "transaction_time": "2025-02-17T08:34:36Z",
        "PhoneNumber": 78546241,
        "added_at": "2025-02-17T09:34:49.183355Z",
        "updated_at": "2025-02-17T09:34:49.183384Z",
        "account": [
            2
        ]
    }
]

```
---

### 2. C2B Data.
**url**: /api/c2b-transactions/
**method**: GET
**header**: Bearer Token (Access token)
```
**Output**:
```json
[
    {
        "id": 1,
        "transaction_id": "12ER334R45",
        "phone_number": "+0722699426",
        "amount": "1458.01",
        "transaction_time": "2025-02-17T09:40:22Z",
        "raw_response": {
            "FKFIT": 5895
        },
        "added_at": "2025-02-17T09:50:56.648398Z",
        "updated_at": "2025-02-17T09:50:56.648432Z",
        "account": [
            2
        ]
    },
    {
        "id": 2,
        "transaction_id": "ASAS",
        "phone_number": "04578452878",
        "amount": "324.00",
        "transaction_time": "2025-02-17T08:51:20Z",
        "raw_response": {
            "FKFIT": 5895
        },
        "added_at": "2025-02-17T09:51:28.546294Z",
        "updated_at": "2025-02-17T09:51:28.546326Z",
        "account": [
            2
        ]
    }
]
```
---

### 3. B2C Data.
**url**: /api/b2c-transactions/
**method**: GET
**header**: Bearer Token (Access token)
```
**Output**:
```json
[
    {
        "id": 1,
        "conversation_id": "ASA12343R4T54FG",
        "originator_conversation_id": "212143R4ER34R",
        "transaction_id": "1212321414123421",
        "result_code": "0",
        "result_desc": "0",
        "amount": "21144.00",
        "receiver_name": "JSMRD",
        "completed_time": "SWSSRG",
        "charges": "02",
        "currency": "KSH",
        "raw_response": {
            "FKFIT": 5895
        },
        "added_at": "2025-02-17T09:57:40.589319Z",
        "updated_at": "2025-02-17T09:57:40.589477Z",
        "account": [
            2
        ]
    },
    {
        "id": 2,
        "conversation_id": "12e3e2e3242",
        "originator_conversation_id": "23d342332223",
        "transaction_id": "dd23e2344422",
        "result_code": "233333",
        "result_desc": "2",
        "amount": "2547.01",
        "receiver_name": "32232332",
        "completed_time": "2323232",
        "charges": "233232",
        "currency": "KSH",
        "raw_response": {
            "FKFIT": 5895
        },
        "added_at": "2025-02-17T09:58:22.912616Z",
        "updated_at": "2025-02-17T09:58:22.912688Z",
        "account": [
            2
        ]
    }
]
```
---