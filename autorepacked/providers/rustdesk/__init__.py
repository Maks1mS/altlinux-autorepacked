import subprocess

from autorepacked.base_provider import BaseProvider


class RustdeskProvider(BaseProvider):
    _name = 'rustdesk'
    _release_url = 'https://github.com/rustdesk/rustdesk/releases'
    _release_file = '[0-9]/rustdesk-[0-9].[0-9].[0-9].deb'

    def get_download_url(self):
        url = subprocess.run(
            args=[
                'epm',
                '--silent',
                'tool',
                'eget',
                '--list',
                '--latest',
                '--get-real-url',
                self._release_url,
                self._release_file,
            ],
            stdout=subprocess.PIPE
        ).stdout.decode('utf-8')

        return url


def get_provider(config):
    return RustdeskProvider(config)
