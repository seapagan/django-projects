"""Define any forms used in the project."""

# ruff: noqa:  RUF012,E501
from django import forms
from django_recaptcha.fields import ReCaptchaField  # type: ignore
from django_recaptcha.widgets import ReCaptchaV2Checkbox  # type: ignore

from app.models import ContactSubmission


class ContactForm(forms.ModelForm[ContactSubmission]):
    """Define the Contact Form using ModelForm."""

    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(),
        error_messages={
            "required": "Please tick the box to prove you are not a robot.",
        },
    )

    class Meta:
        """Meta class for ContactForm."""

        common_input_classes = "appearance-none bg-card border border-border text-foreground placeholder-muted-foreground rounded w-full py-2 px-3 leading-tight focus:outline-none focus:ring focus:ring-ring/50 transition-colors"

        model = ContactSubmission
        fields = ("name", "email", "message")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": common_input_classes,
                    "required": True,
                    "placeholder": "Enter your Name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": common_input_classes,
                    "required": True,
                    "placeholder": "Enter your Email",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": common_input_classes,
                    "rows": 6,
                    "required": True,
                    "placeholder": "Type your Message",
                }
            ),
            "captcha": ReCaptchaField(),
        }
