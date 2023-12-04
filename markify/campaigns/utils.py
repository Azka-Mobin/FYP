from django.core.mail import send_mail
from django.conf import settings


def send_email_to_client():
    subject = "You Might be Interested in This Product"
    message = "Hello, Check this out!"
    from_email = settings.EMAIL_HOST_USER
    
    recipient_list = ["ammarasim065@gmail.com"]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)