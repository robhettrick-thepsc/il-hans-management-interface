import json
from http import HTTPStatus

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.operationoutcome import OperationOutcome, OperationOutcomeIssue
from fhir.resources.organization import Organization

from .models import CareProviderLocation


@csrf_exempt
def care_provider_search(request):
    if request.method == "POST":

        try:
            nhs_number_hash = request.POST["_careRecipientPseudoId"]
        except KeyError:
            operation_outcome_issue = OperationOutcomeIssue(
                severity="error",
                code="required",
                diagnostics="Required search parameter was missing: _careRecipientPseudoId",
            )
            operation_outcome = OperationOutcome(issue=[operation_outcome_issue])
            return JsonResponse(json.loads(operation_outcome.json()), status=HTTPStatus.BAD_REQUEST)

        try:
            care_provider = CareProviderLocation.objects.get(carerecipient__nhs_number_hash=nhs_number_hash)
        except CareProviderLocation.DoesNotExist:
            operation_outcome_issue = OperationOutcomeIssue(
                severity="error",
                code="not-found",
                diagnostics="No subscription was found on the system for the given psuedonymous identifier",
            )
            operation_outcome = OperationOutcome(issue=[operation_outcome_issue])
            return JsonResponse(json.loads(operation_outcome.json()), status=HTTPStatus.NOT_FOUND)

        fhir_contact_point = ContactPoint(system="email", value=care_provider.email, use="work")
        fhir_organization = Organization(name=care_provider.name, telecom=[fhir_contact_point])
        return JsonResponse(json.loads(fhir_organization.json()), safe=False)

    # if not allowed method was used on this endpoint
    operation_outcome_issue = OperationOutcomeIssue(
        severity="error", code="not-allowed", diagnostics="Method not allowed - _search only supports POST"
    )
    operation_outcome = OperationOutcome(issue=[operation_outcome_issue])
    return JsonResponse(json.loads(operation_outcome.json()), status=HTTPStatus.METHOD_NOT_ALLOWED)
