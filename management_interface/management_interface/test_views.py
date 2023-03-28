from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import RegisteredManager


class CareProviderLocationTests(TestCase):
    def setUp(self) -> None:
        self.manager = RegisteredManager.objects.create(
            given_name="Jehosephat", family_name="McGibbons", cqc_registered_manager_id="My CQC RegsiteredManagerID"
        )
        self.location = self.manager.careproviderlocation_set.create(
            name="My Location Name",
            email="nosuchaddress@nhs.net",
            ods_code="My Ods Code",
            cqc_location_id="My CQC Location ID",
        )
        self.care_recipient = self.location.carerecipient_set.create(
            subscription_id="42", provider_reference_id="foobar"
        )
        self.care_recipient.nhs_number = "password"
        self.care_recipient.save()

    def assertFailure(self, response, expected_status_code, expected_code):
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.json()["issue"][0]["code"], expected_code)

    def test_search_get_method_not_allowed(self):
        url = reverse("care_provider_search")
        response = self.client.get(url, {"_careRecipientPseudoId": self.care_recipient.nhs_number_hash})
        self.assertFailure(response, HTTPStatus.METHOD_NOT_ALLOWED, "not-allowed")

    def test_successful_search(self):
        url = reverse("care_provider_search")
        response = self.client.post(url, {"_careRecipientPseudoId": self.care_recipient.nhs_number_hash})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()["name"], self.location.name)

    def test_search_not_found(self):
        url = reverse("care_provider_search")
        response = self.client.post(url, {"_careRecipientPseudoId": "not_existing_id"})
        self.assertFailure(response, HTTPStatus.NOT_FOUND, "not-found")

    def test_search_missing_param_returns_bad_request(self):
        url = reverse("care_provider_search")
        response = self.client.post(url, {})
        self.assertFailure(response, HTTPStatus.BAD_REQUEST, "required")
