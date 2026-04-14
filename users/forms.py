from allauth.account.forms import SignupForm
from django import forms
from .models import Role
from phonenumber_field.formfields import PhoneNumberField

class CustomSignupForm(SignupForm):

    whatsapp_number = PhoneNumberField(
        required=True,
        region="MU"
    )

    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        required=True,
        empty_label="Select a role"
    )

    def save(self, request):
        user = super().save(request)

        user.role = self.cleaned_data["role"]
        user.whatsapp_number = self.cleaned_data["whatsapp_number"]

        user.save()
        return user