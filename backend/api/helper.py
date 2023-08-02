
import uuid
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import requests




ANYMAIL = settings.ANYMAIL



# recipient_email = "ssaimsheikh863@gmail.com"
subject = "Hello"
# message = "Testing some Mailgun awesomeness!"






def send_(recipient_email, subject, message):
    print("send_")
    response = requests.post(
        "https://api.mailgun.net/v3/sandbox7eec2002e12a43cc830980dd86c463b8.mailgun.org/messages",
        auth=("api", 'a4426ae9802f89ce3932509c4113609b-102c75d8-3661c0db'),
        data={"from": "Rose Queen <mailgun@sandbox7eec2002e12a43cc830980dd86c463b8.mailgun.org>",
              "to": recipient_email,
              "subject": subject,
              "text": message})
    try:
        response.raise_for_status()
        print("Email sent successfully.")
    except Exception as e:
        print("An error occurred: {}".format(str(e)))

def send_forget_password_email(email, token):
    print("token",token)
    recipient_email = email
    message=f'Hi, click on the link to reset your password http://127.0.0.1:3000/resetpassword/{token}'
    send_(recipient_email, subject, message)

