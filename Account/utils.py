from django.conf import settings
from django.core.mail import send_mail



def forgot_mail(user):
        
    subject = 'Forgot Password mail'
    message = f'Hi  {user.username} , your password is {user.raw_password}\n thanks.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail( subject, message, email_from, recipient_list )
