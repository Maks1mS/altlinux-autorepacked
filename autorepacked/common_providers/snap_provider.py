import json
import urllib

from autorepacked.common_providers.base_provider import BaseProvider
from urllib.request import Request, urlopen

class SnapProvider(BaseProvider):
    _package_name = "package"
    _channel = "stable"
    _arch = "amd64"

    def _get_snap_info(self):
        request = Request(
            f"http://api.snapcraft.io/v2/snaps/info/{self._package_name}",
            headers={"Content-Type": "application/json", "Snap-Device-Series": "16"},
        )
        response = urlopen(request).read()
        return json.loads(response)

    def get_download_name(self):
        return f"{self._package_name}-{self.get_version()}.snap"

    def get_version(self):
        snap_info = self._get_snap_info()
        for channel_map in snap_info["channel-map"]:
            if (channel_map["channel"]["name"] == self._channel
                    and channel_map["channel"]["architecture"] == self._arch):
                return channel_map['version']

    def get_download_url(self):
        snap_info = self._get_snap_info()
        for channel_map in snap_info["channel-map"]:
            if (channel_map["channel"]["name"] == self._channel
                    and channel_map["channel"]["architecture"] == self._arch):
                return channel_map['download']['url']
