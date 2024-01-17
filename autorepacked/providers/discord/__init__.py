from autorepacked.common_providers.base_provider import BaseProvider


class DiscordProvider(BaseProvider):
    _name = 'discord'

    DOWNLOAD_URL = "https://discord.com/api/download?platform=linux&format=deb"


def get_provider(config):
    return DiscordProvider(config)
