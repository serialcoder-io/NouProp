from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Offer

class OfferForm(forms.ModelForm):
    whatsapp_contact_allowed = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox',
        }),
        label='Allow WhatsApp'
    )

    whatsapp_number = PhoneNumberField(
        region="MU",
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered focus:outline-none focus:ring-0 focus:border-primary',
            'placeholder': 'xxxx xxxx'
        }),
        label='WhatsApp Number',
        required=False
    )

    class Meta:
        model = Offer
        fields = ['whatsapp_contact_allowed', 'whatsapp_number', 'message']