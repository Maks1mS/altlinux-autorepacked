from autorepacked.common_providers.snap_provider import SnapProvider


class SingularityApp(SnapProvider):
    disabled = True

    _name = 'singularityapp'
    _package_name = 'singularityapp'


def get_provider(config):
    return SingularityApp(config)
