import os
import shutil
import tempfile
import re

from autorepacked import utils


def _get_file(directory):
    files_and_dirs = os.listdir(directory)
    files = [f for f in files_and_dirs if os.path.isfile(os.path.join(directory, f))]
    return os.path.join(directory, files[0]) if files else None


class BaseProvider:
    def __init__(self, config):
        self.config = config

    DOWNLOAD_URL = ''
    _name = ''

    def get_name(self):
        return self._name

    def get_version(self):
        url = utils.run([
            'epm',
            '--silent',
            'tool',
            'eget',
            '--get-real-url',
            self.get_download_url(),
        ])

        pattern = r'\d+\.\d+\.\d+'
        match = re.search(pattern, url)
        if match:
            return match.group()
        else:
            return "not found"

    def get_download_url(self):
        return self.DOWNLOAD_URL

    def download(self):
        download_directory = tempfile.mkdtemp()
        repacked_directory = tempfile.mkdtemp()

        utils.run([
            'epm',
            '--silent',
            'tool',
            'eget',
            '-q',
            self.get_download_url(),
        ], cwd=download_directory)

        file = _get_file(download_directory)

        utils.run([
            'epm',
            '--silent',
            '-y',
            'repack',
            file,
        ], cwd=repacked_directory)

        shutil.rmtree(download_directory)

        file = _get_file(repacked_directory)

        utils.run([
            'epm',
            '--silent',
            'repo',
            'pkgadd',
            self.config.get('repo_path'),
            file,
        ], cwd=repacked_directory)

        shutil.rmtree(repacked_directory)
