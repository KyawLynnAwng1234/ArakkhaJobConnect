from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.template.loader import render_to_string
from django.conf import settings
import datetime


def send_verification_email(request, user):
    """
    Sends employer verification email using Django + Anymail MailerSend backend.
    Returns True on success, False on failure.
    """

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    verify_url = request.build_absolute_uri(
        reverse(
            "employer-emailverifypage",
            kwargs={"uidb64": uid, "token": token}
        )
    )

    subject = "Verify Your Employer Account"

    # Fallback text email
    text_content = (
        f"Hello {user.email},\n\n"
        f"Please verify your employer account using the link below:\n"
        f"{verify_url}\n\n"
        f"If you didn't request this, you can ignore this email."
    )

    # HTML version
    html_content = render_to_string(
        "emails/employer_email_verify.html",
        {
            "email": user.email,
            "verify_url": verify_url,
            "year": datetime.datetime.now().year,
        },
    )

    try:
        # Prepare the email message
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=f"{settings.MAILERSEND_FROM_NAME} <{settings.DEFAULT_FROM_EMAIL}>",
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")

        # Try sending using Anymail
        msg.send(fail_silently=False)

        return True   # SUCCESS

    except Exception as e:
        # Log error safely
        print("EMPLOYER EMAIL SEND ERROR:", e)
        return False  # FAILURE
