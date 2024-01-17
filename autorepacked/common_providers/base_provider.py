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
    disabled = False

    def __init__(self, config):
        self.config = config

    DOWNLOAD_URL = ''
    _name = ''

    def get_name(self):
        return self._name

    def get_version(self):
        url = utils.eget([
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

    def get_download_name(self):
        return ""

    def download(self):
        download_directory = tempfile.mkdtemp()
        repacked_directory = tempfile.mkdtemp()

        args = []

        download_name = self.get_download_name()

        if download_name:
            args += ["-O", download_name]

        args += [self.get_download_url()]

        utils.eget(args, cwd=download_directory)

        file = _get_file(download_directory)

        utils.epm([
            '-y',
            'repack',
            file,
        ], cwd=repacked_directory)

        shutil.rmtree(download_directory)

        file = _get_file(repacked_directory)

        utils.epm([
            'repo',
            'pkgadd',
            self.config.get('repo_path'),
            file,
        ], cwd=repacked_directory)

        shutil.rmtree(repacked_directory)
