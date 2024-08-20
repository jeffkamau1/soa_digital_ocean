from postmarker.core import PostmarkClient
from django.core.mail import send_mail
from django.urls import reverse


def send_verification_email(user):
    # Initialize Postmark client with your API token
    try:
        postmark = PostmarkClient(server_token='e7547caf-5cf9-48f4-9116-5e54cddad658')
        verification_link = reverse('verify_email', args=[user.email_verification_token])

        # Define email content
        email_content = {
            'From': 'jeff.kamau@prodapt.com',  # Replace with your sender email address
            'To': user.email,
            'TemplateId': 35530351,  # Replace with your template ID
            'TemplateModel': {
                'name': user.first_name,
                'verification_link': f"http://165.232.176.207:8000{verification_link}"
            }
        }

        # Send email
        response = postmark.emails.send(email_content)
        return response
    except Exception as e:
        return f"Verification email was not sent successfully {e}"
