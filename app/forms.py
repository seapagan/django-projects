"""Define any forms used in the project."""

from django import forms

from app.models import ContactSubmission


class ContactForm(forms.ModelForm):
    """Define the Contact Form using ModelForm."""

    class Meta:
        """Meta class for ContactForm."""

        model = ContactSubmission
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                    "required": True,
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                    "rows": 6,
                    "required": True,
                }
            ),
        }
