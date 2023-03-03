from django.contrib import admin

from .models import (
    CareRecipient,
    CareProviderLocation,
    RegisteredManager,
)

from .forms import (
    CareProviderLocationForm,
    RegisteredManagerForm,
    CareRecipientForm
)


@admin.register(CareRecipient)
class CareRecipientAdmin(admin.ModelAdmin):
    search_fields = ("nhs_number_hash", "provider_reference_id",)
    list_filter = ("care_provider_location_id",)
    form = CareRecipientForm


@admin.register(RegisteredManager)
class RegisteredManagerAdmin(admin.ModelAdmin):
    form = RegisteredManagerForm
    pass


@admin.register(CareProviderLocation)
class CareProviderLocationAdmin(admin.ModelAdmin):
    form = CareProviderLocationForm
    pass
