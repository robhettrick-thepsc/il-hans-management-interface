from django import forms

from .models import CareProviderLocation, CareRecipient, RegisteredManager


class CareProviderLocationForm(forms.ModelForm):
    class Meta:
        model = CareProviderLocation
        exclude = ["id", "created_at", "updated_at"]


class RegisteredManagerForm(forms.ModelForm):
    class Meta:
        model = RegisteredManager
        exclude = ["id", "created_at", "updated_at"]
        labels = {
            "cqc_registered_manager_id": "CQC Registered Manager ID",
        }


class CareRecipientForm(forms.ModelForm):
    class Meta:
        model = CareRecipient
        exclude = ["id", "created_at", "updated_at"]
        labels = {
            "nhs_number": "NHS Number",
        }
