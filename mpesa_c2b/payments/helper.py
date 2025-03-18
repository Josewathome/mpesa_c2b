import json
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from .models import Account
from .serializers import AccountSerializer_1

def Token_Auth(unique_code, user):
    refresh = RefreshToken.for_user(user)
    refresh['username'] = user.username
    refresh['email'] = user.email
    refresh['unique_code'] = str(unique_code)
    access_token = str(refresh.access_token)
    return refresh, access_token

def send_email_mail(verification_code, user_email, user_name):
    subject = "Account Verification"
    current_year = datetime.now().year
    # HTML email body
    html_email_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Account Verification</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f9;
                color: #333;
                line-height: 1.6;
            }}
            .email-container {{
                max-width: 600px;
                margin: 20px auto;
                background: #ffffff;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            .header {{
                background-color: #4CAF50;
                padding: 20px;
                text-align: center;
            }}
            .header img {{
                max-width: 150px;
                height: auto;
            }}
            .content {{
                padding: 20px;
            }}
            .content h2 {{
                color: #4CAF50;
                text-align: center;
            }}
            .content p {{
                margin: 15px 0;
            }}
            .content h3 {{
                color: #4CAF50;
                font-size: 18px;
            }}
            .content ul {{
                list-style: none;
                padding: 0;
            }}
            .content ul li {{
                margin: 10px 0;
            }}
            .content ul li a {{
                color: #1E90FF;
                text-decoration: none;
            }}
            .content ul li a:hover {{
                text-decoration: underline;
            }}
            .footer {{
                background-color: #f4f4f9;
                text-align: center;
                padding: 10px;
                font-size: 12px;
                color: #888;
            }}
            @media screen and (max-width: 600px) {{
                .content h2, .content h3 {{
                    font-size: 20px;
                }}
                .content p {{
                    font-size: 14px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <img src="https://drive.google.com/uc?id=1eken9vH3A7wCsbw1aNUAhb_vOXMnoWSw" alt="Logo">
            </div>
            <div class="content">
                <h2>Account Verification</h2>
                <p>Hi <strong>{user_name}</strong>,</p>
                <p>Your account verification code is:</p>
                <h3>{verification_code}</h3>
                <p>If you did not Request for this Verification Code Please Ignore</p>
                <p>Use the links below to proceed:</p>
                <ul>
                    <li><a href="https://Mkash.com/">Learn More</a></li>
                    
                </ul>
                <p>If you have any questions, feel free to contact our support team.</p>
                <p>Thank you!</p>
            </div>
            <div class="footer">
                &copy; {current_year} Mkash. All rights reserved.
            </div>
        </div>
    </body>
    </html>
    """
    # done by @Josewathome (git) dont Touch
    # Send email
    """send_mail(
        subject,
        '',  # Plain text version can be empty if not needed
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
        html_message=html_email_body  # Set HTML content
    )"""
    print("Email Sent")
    
def get_Account_details(unique_code):
    account = get_object_or_404(Account, unique_code=unique_code)
    serializer = AccountSerializer_1(account)
    return json.loads(json.dumps(serializer.data))