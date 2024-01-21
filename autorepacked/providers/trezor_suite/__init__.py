from autorepacked.common_providers.github_releases_provider import GithubReleasesProvider


class TrezorSuiteProvider(GithubReleasesProvider):
    _name = 'trezor-suite'

    _repo = 'trezor/trezor-suite'

    def _last_tag_name(self):
        return f'v{self.get_version()}'

    def _get_release_filename(self):
        return f'Trezor-Suite-{self.get_version()}-linux-x86_64.AppImage'

    def get_download_name(self):
        return f"trezor-suite-{self.get_version()}-linux-x86_64.AppImage"


def get_provider(config):
    return TrezorSuiteProvider(config)
