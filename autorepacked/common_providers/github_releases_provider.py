import re

from autorepacked import utils
from autorepacked.common_providers.base_provider import BaseProvider


class GithubReleasesProvider(BaseProvider):
    _repo = ''

    def _last_release_url(self):
        return utils.eget([
            '--get-real-url',
            f'https://github.com/{self._repo}/releases/latest'
        ])

    def _last_tag_name(self):
        return self.get_version()

    def _get_release_filename(self):
        return ''

    def get_version(self):
        url = self._last_release_url()

        pattern = r'\d+\.\d+\.\d+'
        match = re.search(pattern, url)
        if match:
            return match.group()
        else:
            return "not found"

    def get_download_url(self):
        return (f"https://github.com/"
                f"{self._repo}/releases/download/"
                f"{self._last_tag_name()}/{self._get_release_filename()}")
