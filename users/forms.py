from allauth.account.forms import SignupForm
from django import forms
from .models import Role, User
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


class UserAccountForm(forms.ModelForm):
    def __init__(self, *args, user_has_social_account=False, **kwargs):
        super().__init__(*args, **kwargs)

        if user_has_social_account:
            self.fields["email"].disabled = True
            self.fields["email"].help_text = "Email cannot be changed for social login accounts"

    class Meta:
        model = User
        fields = ["email", "display_name", "whatsapp_number"]
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Email address",
            }),
            "display_name": forms.TextInput(attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Display name",
            }),
            "whatsapp_number": forms.TextInput(attrs={
                "class": "input input-bordered w-full",
                "placeholder": "WhatsApp number",
            }),
        }


class DeleteAccountForm(forms.Form):
    confirmation_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Type your email to confirm",
        })
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_confirmation_email(self):
        confirmation_email = self.cleaned_data["confirmation_email"]
        if self.user and confirmation_email != self.user.email:
            raise forms.ValidationError("Enter your current account email to confirm deletion.")
        return confirmation_email
