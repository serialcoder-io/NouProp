from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Offer, Listing


class OfferForm(forms.ModelForm):
    whatsapp_contact_allowed = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': '',
        }),
        label='Allow publisher to contact you via WhatsApp'
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


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['category', 'area', 'title', 'description', 'image', 'is_free', 'price', 'is_open']

        widgets = {
            'category': forms.Select(
                attrs={
                    'class': 'select select-bordered focus:outline-none focus:ring-0 focus:border-primary',
                }
            ),
            'area': forms.Select(
                attrs={
                    'class': 'select select-bordered focus:outline-none focus:ring-0 focus:border-primary',
                }
            ),
            'title': forms.TextInput(
                attrs={
                    'class': 'input input-bordered focus:outline-none focus:ring-0 focus:border-primary',
                    'placeholder': 'Enter listing title',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'textarea textarea-bordered focus:outline-none focus:ring-0 focus:border-primary',
                    'placeholder': 'Enter description',
                    'rows': '5',
                }
            ),
            'image': forms.FileInput(
                attrs={
                    'class': 'file-input file-input-bordered',
                }
            ),
            'is_free': forms.CheckboxInput(
                attrs={
                    'class': '',
                }
            ),
            'is_open': forms.CheckboxInput(
                attrs={
                    'class': '',
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'input input-bordered focus:outline-none focus:ring-0 focus:border-primary',
                    'placeholder': '0.00',
                    'step': '0.01',
                }
            ),
        }