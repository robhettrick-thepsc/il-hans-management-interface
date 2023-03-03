from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import CareProviderLocation, RegisteredManager, CareRecipient

def assert_rejects_email(obj, email):
    obj.email = email
    try:
        obj.full_clean()
    except ValidationError as e:
        assert('email' in e.message_dict)
        assert('Enter an nhs.net email address' in e.message_dict['email'])

def assert_accepts_email(obj, email):
    obj.email = email
    try:
        obj.full_clean()
    except ValidationError as e:
        assert('email' not in e.message_dict)


class RegisteredManagerTests(TestCase):
    def test_rejects_bad_email_domain(self):
        assert_rejects_email(RegisteredManager(), "bad-man@invalid-domain.evil")

    def test_accepts_safe_email_domain(self):
        assert_accepts_email(RegisteredManager(), "good-dr@nhs.net")

    def test_rejects_invalid_email_address_format(self):
        assert_rejects_email(RegisteredManager(), "notanemail.address")

    def test_accepts_data_fields(self):
        manager = RegisteredManager(given_name="Jehosephat",
                                    family_name="McGibbons",
                                    cqc_registered_manager_id="My CQC Registered Manager ID")

        try:
            manager.full_clean()
        except ValidationError as e:
            assert('given_name' not in e.message_dict)
            assert('first_name' not in e.message_dict)
            assert('cqc_registered_manager_id' not in e.message_dict)


class CareProviderLocationTests(TestCase):
    def test_rejects_bad_email_domain(self):
        assert_rejects_email(CareProviderLocation(), "bad-man@invalid-domain.evil")

    def test_accepts_safe_email_domain(self):
        assert_accepts_email(CareProviderLocation(), "good-dr@nhs.net")

    def test_rejects_invalid_email_address_format(self):
        assert_rejects_email(CareProviderLocation(), "notanemail.address")

    def test_accepts_data_fields(self):
        location = CareProviderLocation(name="My Location Name",
                                        ods_code="My Ods Code",
                                        cqc_location_id="My CQC Location ID")

        try:
            location.full_clean()
        except ValidationError as e:
            assert('name' not in e.message_dict)
            assert('ods_code' not in e.message_dict)
            assert('cqc_location_id' not in e.message_dict)

    def test_wont_save_without_a_manager(self):
        location = CareProviderLocation(name="My Location Name",
                                        email="nosuchaddress@nhs.net",
                                        ods_code="My Ods Code",
                                        cqc_location_id="My CQC Location ID")
        with self.assertRaises(Exception):
            location.save()

    def test_saves_with_a_manager(self):
        manager = RegisteredManager(given_name="Jehosephat",
                                    family_name="McGibbons",
                                    cqc_registered_manager_id="My CQC RegsiteredManagerID")
        manager.save()
        location = CareProviderLocation(registered_manager_id=manager,
                                        name="My Location Name",
                                        email="nosuchaddress@nhs.net",
                                        ods_code="My Ods Code",
                                        cqc_location_id="My CQC Location ID")
        location.save()

class CareRecipientTests(TestCase):
    def test_stores_nhs_number_as_hash(self):
        jeff = CareRecipient()
        # These magic values are taken from the scrypt spec
        jeff.nhs_number = "password"
        self.assertEquals(jeff.nhs_number_hash,
                          bytearray([0xfd, 0xba, 0xbe, 0x1c, 0x9d, 0x34, 0x72, 0x00,
                                     0x78, 0x56, 0xe7, 0x19, 0x0d, 0x01, 0xe9, 0xfe,
                                     0x7c, 0x6a, 0xd7, 0xcb, 0xc8, 0x23, 0x78, 0x30,
                                     0xe7, 0x73, 0x76, 0x63, 0x4b, 0x37, 0x31, 0x62,
                                     0x2e, 0xaf, 0x30, 0xd9, 0x2e, 0x22, 0xa3, 0x88,
                                     0x6f, 0xf1, 0x09, 0x27, 0x9d, 0x98, 0x30, 0xda,
                                     0xc7, 0x27, 0xaf, 0xb9, 0x4a, 0x83, 0xee, 0x6d,
                                     0x83, 0x60, 0xcb, 0xdf, 0xa2, 0xcc, 0x06, 0x40]))

    def test_nhs_number_is_write_only(self):
        jeff = CareRecipient()
        jeff.nhs_number = "super-sekrit"
        with self.assertRaises(Exception):
            jeff.nhs_number

    def test_nhs_number_hash_gets_saved(self):
        manager = RegisteredManager.objects.create(given_name="Jehosephat",
                                                   family_name="McGibbons",
                                                   cqc_registered_manager_id="My CQC RegsiteredManagerID")
        location = manager.careproviderlocation_set.create(name="My Location Name",
                                                          email="nosuchaddress@nhs.net",
                                                          ods_code="My Ods Code",
                                                          cqc_location_id="My CQC Location ID")
        jeff = location.carerecipient_set.create(subscription_id="42",
                                                 provider_reference_id="foobar")
        # These magic values are taken from the scrypt spec
        jeff.nhs_number = "password"
        jeff.save()

        jeff_comparison = CareRecipient.objects.get(pk=jeff.id)
        self.assertEquals(jeff.nhs_number_hash_bytes, jeff_comparison.nhs_number_hash_bytes)
