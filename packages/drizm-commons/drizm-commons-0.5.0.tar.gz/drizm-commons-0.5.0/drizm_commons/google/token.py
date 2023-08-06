import requests
import requests.adapters
import google.auth.exceptions
from google.oauth2 import service_account
from google.oauth2._client import id_token_jwt_grant  # noqa protected
from google.auth.transport.requests import Request


def construct_service_authentication_request() -> Request:
    auth_request_session = requests.Session()
    retry_adapter = requests.adapters.HTTPAdapter(max_retries=3)
    auth_request_session.mount("https://", retry_adapter)
    auth_request = Request(auth_request_session)
    return auth_request


def force_obtain_id_token(credentials: service_account.IDTokenCredentials) -> str:
    """
    Can be used to obtain an OIDC-Token for authenticating
    to GoogleCloud services and some Google APIs.

    This is effectively manually forcing the equivalent of `credentials.refresh()`.

    Examples:
        ```python
        from drizm_commons.google import force_obtain_id_token
        from google.oauth2 import service_account


        auth = service_account.IDTokenCredentials.from_service_account_file(
            "/path/to/svc.json",
            target_audience="https://example.com/"
        )
        token = force_obtain_id_token(auth)
        ```

    Returns:
        Returns a Google OpenID-Connect access token as a string.
    """
    assertion = credentials._make_authorization_grant_assertion()  # noqa protected
    request = construct_service_authentication_request()
    try:
        access_token, *_ = id_token_jwt_grant(
            request,
            credentials._token_uri,  # noqa protected
            assertion,  # noqa expected type
        )
    except google.auth.exceptions.RefreshError as exc:
        raise Exception(
            "Error when requesting the token, "
            "you may have provided an empty target_audience parameter,"
            " for the Credentials object."
        ) from exc
    return access_token


__all__ = ["force_obtain_id_token", "construct_service_authentication_request"]
