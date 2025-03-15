"""Define any forms used in the project."""

from django import forms


class ContactForm(forms.Form):
    """Define the Contact Form."""

    name = forms.CharField(
        label="Your Name",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                "required": True,
            }
        ),
    )
    email = forms.EmailField(
        label="Your Email",
        widget=forms.EmailInput(
            attrs={
                "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                "required": True,
            }
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                "rows": 6,
                "required": True,
            }
        ),
    )
