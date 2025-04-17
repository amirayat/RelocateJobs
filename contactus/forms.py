from django import forms

from .models import ContactUs


class ContactForm(forms.ModelForm):
    """
    contact model form
    """
    class Meta:
        model = ContactUs
        fields = [
            'subject',
            'email',
            'description'
        ]
    
