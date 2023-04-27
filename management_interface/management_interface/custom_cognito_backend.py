from django_cognito_saml.backends import SuperUserBackend


class CustomCognitoBackend(SuperUserBackend):
    create_unknown_user = True

    def authenticate(  # type: ignore[override]
            self, request: HttpRequest, cognito_jwt: dict[str, Any], **kwargs: Any
    ) -> Optional[AbstractBaseUser]:
        remote_user = cognito_jwt["email"]
        user = super().authenticate(request, remote_user=remote_user, **kwargs)
        return user

    def configure_user(  # type: ignore[override]
            self, request: HttpRequest, user: AbstractBaseUser, **kwargs: Any
    ) -> AbstractBaseUser:
        print("In configure_user")
        if created:
            user.name = self.cognito_jwt["email"]
            user.is_admin = True
            user.has_perm = True
            user.has_module_perms = True
            user.is_staff = True
            user.save()
        return user
