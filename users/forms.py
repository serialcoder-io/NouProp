# users/forms.py

from allauth.account.forms import SignupForm
from django import forms
from .models import Role

class CustomSignupForm(SignupForm):
    display_name = forms.CharField(max_length=50, required=True)

    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        required=True,
        empty_label="Select a role"
    )

    def save(self, request):
        user = super().save(request)

        user.display_name = self.cleaned_data['display_name']
        user.role = self.cleaned_data['role']
        user.save()

        return user