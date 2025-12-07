import random
import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_verification_code(user):
    """
    Sends OTP using Django + Anymail MailerSend backend.
    Returns OTP on success, None on failure.
    """
    otp_code = str(random.randint(100000, 999999))
    subject = "Your Email Verification Code"

    jobseeker_name = user.email.split("@")[0]

    # Build email HTML
    html_content = render_to_string(
        "emails/otp_verification.html",
        {
            "username": jobseeker_name,
            "otp_code": otp_code,
            "year": datetime.datetime.now().year,
        },
    )

    # Plain text version
    text_content = (
        f"Hello {jobseeker_name},\n\n"
        f"Your OTP verification code is: {otp_code}\n"
        f"This code expires in 5 minutes.\n\n"
        f"If you did not request this, please ignore this email."
    )

    try:
        # Prepare message
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=f"{settings.MAILERSEND_FROM_NAME} <{settings.DEFAULT_FROM_EMAIL}>",
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")

        # → Try sending email (Anymail backend)
        msg.send(fail_silently=False)

        return otp_code  # SUCCESS

    except Exception as e:
        # → Catch ALL MailerSend/Anymail errors
        print("EMAIL SEND ERROR:", e)
        return None  # FAILURE
