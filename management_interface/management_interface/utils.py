from django.core.exceptions import ValidationError


def validated_email_domain(email: str, domain: str, error_message: str):
    if not email.endswith(domain):
        raise ValidationError(error_message)
    return email
