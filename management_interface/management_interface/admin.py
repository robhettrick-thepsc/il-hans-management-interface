from django.contrib import admin

from .forms import CareProviderLocationForm, CareRecipientForm, RegisteredManagerForm
from .models import CareProviderLocation, CareRecipient, RegisteredManager


def set_obj_created_updated(request, obj, form):
    """
    Updates created_by and updated_by fields if the object was created or changed in admin
    """
    if form.changed_data and obj.created_by:
        obj.updated_by = request.user

    if not obj.created_by:
        obj.created_by = request.user
    return obj


@admin.register(CareRecipient)
class CareRecipientAdmin(admin.ModelAdmin):
    search_fields = (
        "nhs_number_hash",
        "provider_reference_id",
    )
    list_filter = ("care_provider_location_id",)
    form = CareRecipientForm

    def save_model(self, request, obj, form, change):
        obj = set_obj_created_updated(request, obj, form)
        super().save_model(request, obj, form, change)

    def get_exclude(self, request, obj=None):
        exclude = self.exclude
        if obj and obj.nhs_number_hash:
            exclude = ("nhs_number",)
        return exclude


@admin.register(RegisteredManager)
class RegisteredManagerAdmin(admin.ModelAdmin):
    form = RegisteredManagerForm

    def save_model(self, request, obj, form, change):
        obj = set_obj_created_updated(request, obj, form)
        super().save_model(request, obj, form, change)


@admin.register(CareProviderLocation)
class CareProviderLocationAdmin(admin.ModelAdmin):
    form = CareProviderLocationForm

    def save_model(self, request, obj, form, change):
        obj = set_obj_created_updated(request, obj, form)
        super().save_model(request, obj, form, change)
