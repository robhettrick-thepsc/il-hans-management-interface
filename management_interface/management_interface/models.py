import hashlib

from django.db import models
import uuid
from datetime import datetime


class BaseModel(models.Model):
    """
    Base model holding shared data
    """
    id = models.CharField(
        primary_key=True, max_length=64, default=uuid.uuid4, editable=False, unique=True
    )
    created_at = models.DateTimeField(default=datetime.utcnow, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class CareProviderLocation(BaseModel):
    """
    Model that represents a registered care provider location (branch) who wants to receive emails.
    """
    name = models.CharField(max_length=256, help_text="Helping Hands Wantage")
    email = models.EmailField(null=False, db_index=True, unique=True, help_text="example@nhs.net")
    ods_code = models.CharField(null=False, max_length=16, unique=True, help_text="VNJNK")
    cqc_location_id = models.CharField(null=False, max_length=128, unique=True, help_text="1-11086090064")
    registered_manager_id = models.ForeignKey("RegisteredManager", on_delete=models.CASCADE)


class RegisteredManager(BaseModel):
    """
    Model that represents somebody who is a Care Quality Commission (CQC) registered manager.
    """
    given_name = models.CharField(max_length=256, db_index=True, help_text="Aislinn")
    family_name = models.CharField(max_length=256, db_index=True, help_text="Mullen")
    email = models.EmailField(null=False, db_index=True, unique=True, help_text="example@nhs.net")
    cqc_registered_manager_id = models.CharField(max_length=128, help_text="1-XXXXXXXX")


class CareRecipient(BaseModel):
    """
    Model that represents somebody who is receiving care from a care provider location
    and who has had a HANS subscription made for them.
    """

    care_provider_location_id = models.ForeignKey("CareProviderLocation", on_delete=models.CASCADE)
    nhs_number_hash = models.CharField(null=False, max_length=128, db_index=True, editable=False)
    nhs_number = models.CharField(null=True, blank=True, max_length=32)
    subscription_id = models.CharField(null=False, max_length=32, db_index=True, unique=True, editable=False)
    provider_reference_id = models.CharField(null=False, max_length=128, db_index=True, unique=True, help_text="WANT45320482")

    def save(self, *args, **kwargs):
        # to be replaced by Scrypt
        self.nhs_number_hash = hashlib.sha3_256(str(self.nhs_number).encode()).hexdigest()
        self.nhs_number = None
        super().save(*args, **kwargs)
