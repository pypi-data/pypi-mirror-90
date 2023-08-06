import requests

from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import WorldCubeAssociationProvider


class WorldCubeAssociationOAuth2Adapter(OAuth2Adapter):
    provider_id = WorldCubeAssociationProvider.id
    provider_default_url = "https://www.worldcubeassociation.org"
    provider_api_version = "v0"

    settings = app_settings.PROVIDERS.get(provider_id, {})
    provider_base_url = settings.get("BASE_URL", provider_default_url)

    access_token_url = "{0}/oauth/token/".format(provider_base_url)
    authorize_url = "{0}/oauth/authorize/".format(provider_base_url)
    profile_url = "{0}/api/{1}/me".format(provider_base_url, provider_api_version)

    def complete_login(self, request, app, token, response):
        response = requests.get(
            self.profile_url, headers={"Authorization": "Bearer {0}".format(token)}
        )
        extra_data = response.json().get("me")
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(WorldCubeAssociationOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(WorldCubeAssociationOAuth2Adapter)
