from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail


class Util:
    @staticmethod
    def send_email(data):
        print("Sending email to:", data["to_email"])  # Debugging
        send_mail(
            subject=data["mail_subject"],
            message=data["mail_body"],
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[data["to_email"]],
            fail_silently=False,
        )
        
def activation_mail(user):
    """
    Generates email data for user activation with a direct backend API link.
    """
    mail_subject = "Verify your Account."
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    
    activation_link = f"{settings.BASE_BACKEND_URL}/api/accounts/email-activation/{uid}/{token}/"

    send_mail_data = {
        "mail_subject": mail_subject,
        "mail_body": activation_link,  
        "to_email": user.email_address,
    }

    return send_mail_data
