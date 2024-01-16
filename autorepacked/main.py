import json
import os
import importlib

from autorepacked import utils
from autorepacked.base_provider import BaseProvider
from autorepacked.config import Config


def create_repo(config):
    utils.run([
        'epm',
        'repo',
        'create',
        config.get('repo_path')
    ])


def main():
    config = Config()

    create_repo(config)

    providers_path = os.path.join(os.getcwd(), 'autorepacked/providers')
    modules = os.listdir(providers_path)

    json_file_path = os.path.join(config.get('repo_path'), 'data.json')
    if not os.path.exists(json_file_path):
        with open(json_file_path, 'w') as data_file:
            json.dump({'versions': {}}, data_file, indent=4)

    with open(json_file_path, 'r') as data_file:
        repo_data = json.load(data_file)

    versions = repo_data['versions']
    need_update_index = False
    for module_name in modules:
        module = importlib.import_module(f'providers.{module_name}')
        if hasattr(module, 'get_provider'):
            provider = module.get_provider(config)  # type: BaseProvider
            name = provider.get_name()
            print(f"request version of {name}")
            version = provider.get_version()
            if name not in versions or versions[name] != version:
                print(f'{name} has new version {version}')
                versions[name] = version
                provider.download()
                need_update_index = True

    repo_data['versions'] = versions

    with open(json_file_path, 'w') as data_file:
        json.dump(repo_data, data_file, indent=4)

    if need_update_index:
        utils.run(
            args=[
                'epm',
                'repo',
                'index',
                config.get('repo_path'),
            ]
        )


if __name__ == "__main__":
    main()
