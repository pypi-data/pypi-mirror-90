# -*- coding: utf-8 -*-
"""
|oauth2| Providers
-------------------

Providers which implement the |oauth2|_ protocol.

.. autosummary::

    Authentic
"""
from authomatic.providers.oauth2 import OAuth2
from pas.plugins.imio.utils import protocol

import jwt
import os


__all__ = ["Authentic"]


class Authentic(OAuth2):
    """
    """

    def __init__(self, *args, **kwargs):
        super(Authentic, self).__init__(*args, **kwargs)
        self.user_state = self.params.get("next_url")
        if self.user_state:
            del self.adapter.view.request.form["next_url"]

    def create_request_elements(
        cls,
        request_type,
        credentials,
        url,
        method="GET",
        params=None,
        headers=None,
        body="",
        secret=None,
        redirect_uri="",
        scope="",
        csrf="",
        user_state="",
    ):
        req = super(Authentic, cls).create_request_elements(
            request_type=request_type,
            credentials=credentials,
            url=url,
            method=method,
            params=params,
            headers=headers,
            body=body,
            secret=secret,
            redirect_uri=redirect_uri,
            scope=scope,
            csrf=csrf,
            user_state=cls.user_state,
        )
        return req

    @property
    def base_url(self):
        authentic_hostname = self.settings.config[self.name].get("hostname")
        return "{0}://{1}".format(protocol(), authentic_hostname)

    @property
    def user_authorization_url(self):
        return "{0}/idp/oidc/authorize/".format(self.base_url)

    @property
    def access_token_url(self):
        return "{0}/idp/oidc/token/".format(self.base_url)

    @property
    def user_info_url(self):
        return "{0}/idp/oidc/user_info/".format(self.base_url)

    @property
    def user_api_url(self):
        return "{0}/api/users/".format(self.base_url)

    @property
    def user_info_scope(self):
        return ["openid", "email", "profile", "roles"]

    @staticmethod
    def _x_user_parser(user, data):
        encoded = data.get("id_token")
        if encoded:
            payload_data = jwt.decode(
                encoded,
                algorithms=["RS256"],
                options={"verify_signature": False, "verify_aud": False},
            )
            if "sub" in payload_data.keys():
                user.id = user.username = payload_data.get("sub")
        if "sub" in data.keys():
            # user.id = data.get('sub')
            # user.id = data.get('email')
            user.id = data.get("preferred_username")
            user.username = user.id
            user.first_name = data.get("given_name")
            user.last_name = data.get("family_name")
            fullname = u"{0} {1}".format(user.first_name, user.last_name)
            if not fullname.strip():
                user.name = user.id
                user.fullname = user.id
            else:
                user.name = fullname
                user.fullname = fullname
            roles = data.get("roles", [])
            user.roles = ["Member"]
            if len(roles) > 0:
                app_id = os.environ.get("application_id", "")
                service_slug = os.environ.get("service_slug", "")
                if any("{}-admin".format(app_id) in role for role in roles):
                    user.roles.append("Manager")
                if any("{}-admin".format(service_slug) in role for role in roles):
                    user.roles.append("Site Manager")
        return user


# The provider type ID is generated from this list's indexes!
# Always append new providers at the end
# so that ids of existing providers don't change!
PROVIDER_ID_MAP = [Authentic]
