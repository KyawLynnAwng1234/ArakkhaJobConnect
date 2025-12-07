# JobSeeker/utils/email_service.py

import requests
from django.conf import settings


def send_otp_email(recipient_email: str, otp: str) -> bool:
    """
    Send OTP email to MailerSend using REST API.
    This does NOT require mailersend-python package.
    """

    url = "https://api.mailersend.com/v1/email"

    headers = {
        "Authorization": f"Bearer {settings.MAILERSEND_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "from": {
            "email": settings.MAILERSEND_FROM_EMAIL,
            "name": settings.MAILERSEND_FROM_NAME
        },
        "to": [
            {"email": recipient_email}
        ],
        "subject": "Your OTP Code",
        "html": f"""
            <p>Hello,</p>
            <p>Your OTP code is:</p>
            <h2 style="font-size: 28px; letter-spacing: 4px;"><b>{otp}</b></h2>
            <p>This code expires in 5 minutes.</p>
        """
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print("MailerSend status:", response.status_code)
        print("MailerSend response:", response.text)

        return response.status_code in [200, 202]
    except Exception as e:
        print("MailerSend Error:", e)
        return False
