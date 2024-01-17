from autorepacked.common_providers.github_releases_provider import GithubReleasesProvider


class RustdeskProvider(GithubReleasesProvider):
    _name = 'rustdesk'

    _repo = 'rustdesk/rustdesk'

    def _get_release_filename(self):
        return f'rustdesk-{self.get_version()}-x86_64.deb'


def get_provider(config):
    return RustdeskProvider(config)
