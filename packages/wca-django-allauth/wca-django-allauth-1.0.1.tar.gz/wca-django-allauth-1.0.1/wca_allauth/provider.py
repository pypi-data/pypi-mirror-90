from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class WorldCubeAssociationAccount(ProviderAccount):
    def get_profile_url(self):
        return self.account.extra_data.get("url")

    def get_avatar_url(self):
        return self.account.extra_data.get("avatar", {}).get("url")

    def to_str(self):
        dflt = super().to_str()
        return self.account.extra_data.get("name", dflt)


class WorldCubeAssociationProvider(OAuth2Provider):
    id = "worldcubeassociation"
    name = "worldcubeassociation"
    account_class = WorldCubeAssociationAccount

    def get_default_scope(self):
        return []

    def extract_uid(self, data):
        return str(data["id"])

    def extract_common_fields(self, data):
        return dict(
            name=data.get("name"),
            wca_id=data.get("wca_id"),
        )


provider_classes = [WorldCubeAssociationProvider]
