from autorepacked.common_providers.github_releases_provider import GithubReleasesProvider


class UltimakerCuraProvider(GithubReleasesProvider):
    _name = 'ultimaker-cura'

    _repo = 'Ultimaker/Cura'

    def _get_release_filename(self):
        return f'UltiMaker-Cura-{self.get_version()}-linux.AppImage'

    def get_download_name(self):
        return f"ultimaker-cura-{self.get_version()}-linux-x86_64.AppImage"

    def get_version(self):
        # pin version due to error in start
        return '5.4.0'


def get_provider(config):
    return UltimakerCuraProvider(config)
