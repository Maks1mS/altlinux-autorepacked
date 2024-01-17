from autorepacked.common_providers.base_provider import BaseProvider


class CodeProvider(BaseProvider):
    _name = 'code'

    DOWNLOAD_URL = "https://code.visualstudio.com/sha/download?build=stable&os=linux-rpm-x64"


def get_provider(config):
    return CodeProvider(config)
