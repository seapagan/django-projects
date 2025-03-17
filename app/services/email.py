"""Email service for the application."""

from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from app.models import ContactSubmission


class EmailService:
    """Service class for handling email operations."""

    @staticmethod
    def send_contact_email(submission: ContactSubmission) -> bool:
        """Send contact form submission via email.

        Args:
            submission: The ContactSubmission instance

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            subject = f"New Contact Form Submission from {submission.name}"
            message = render_to_string(
                "app/email/contact_form.txt",
                {
                    "name": submission.name,
                    "email": submission.email,
                    "message": submission.message,
                    "created_at": submission.created_at,
                },
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_FORM_RECIPIENT],
                fail_silently=False,
            )
        except SMTPException:
            return False
        else:
            return True
