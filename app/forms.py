"""Define any forms used in the project."""

# ruff: noqa:  RUF012,E501
from django import forms

from app.models import ContactSubmission


class ContactForm(forms.ModelForm[ContactSubmission]):
    """Define the Contact Form using ModelForm."""

    class Meta:
        """Meta class for ContactForm."""

        model = ContactSubmission
        fields = ("name", "email", "message")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                    "required": True,
                    "placeholder": "Enter your Name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                    "required": True,
                    "placeholder": "Enter your Email",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                    "rows": 6,
                    "required": True,
                    "placeholder": "Type your Message",
                }
            ),
        }
