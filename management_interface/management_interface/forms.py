from django import forms
from .models import CareProviderLocation, RegisteredManager, CareRecipient
from .utils import validated_email_domain


class CareProviderLocationForm(forms.ModelForm):
    class Meta:
        model = CareProviderLocation
        exclude = ["id", "created_at", "updated_at"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        return validated_email_domain(email=email,
                                      domain="nhs.net",
                                      error_message="Care provider e-mail has to be in NHS.net domain")


class RegisteredManagerForm(forms.ModelForm):
    class Meta:
        model = RegisteredManager
        exclude = ["id", "created_at", "updated_at"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        return validated_email_domain(email=email,
                                      domain="nhs.net",
                                      error_message="Registered manager e-mail has to be in NHS.net domain")


class CareRecipientForm(forms.ModelForm):
    class Meta:
        model = CareRecipient
        exclude = ["id", "created_at", "updated_at"]
