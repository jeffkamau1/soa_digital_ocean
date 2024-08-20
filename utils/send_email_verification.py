from postmarker.core import PostmarkClient
from postmarker.models import templates
from postmarker.models.emails import EmailTemplate
from django.core.mail import send_mail
from django.urls import reverse


def send_verification_email(user):
    # Initialize Postmark client with your API token
    try:
        postmark = PostmarkClient(server_token='e7547caf-5cf9-48f4-9116-5e54cddad658')
        verification_link = reverse('verify_email', args=[user.email_verification_token])

        response = postmark.emails.send_with_template(
            TemplateId=35530351,
            TemplateModel={'verification_link': f"http://165.232.176.207:8000{verification_link}"},
            From='jeff.kamau@prodapt.com',
            To=user.email,

        )
        return response
    except Exception as e:
        return f"Verification email was not sent successfully {e}"

# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.shortcuts import render
# from django.utils.html import strip_tags
# from django.urls import reverse
#
#
# def send_verification_email(user):
#     try:
#         # Define email content
#         subject = 'Verification Email'
#         from_email = 'serviceoperationsMPA@outlook.com'  # Replace with your sender email address
#         to_email = user.email
#
#         # Render email template
#         verification_link = reverse('verify_email', args=[user.email_verification_token])
#         template_path = 'email_verification.html'  # Specify the path to your email template
#         context = {'name': user.first_name, 'verification_link': f"http://127.0.0.1:8000{verification_link}"}
#         html_message = render_to_string(template_path, context)
#         plain_message = ""  # Strip HTML tags for plain text message
#
#         # Send email
#         send_mail(subject, plain_message, from_email, [to_email], html_message=html_message, fail_silently=False)
#
#         return True  # Indicate successful email sending
#     except Exception as e:
#         # Return the error
#         return e
