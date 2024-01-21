import datetime
import json
import os
import importlib
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, FastAPI
import uvicorn
from fastapi_utils.tasks import repeat_every

from autorepacked import utils
from autorepacked.common_providers.base_provider import BaseProvider
from autorepacked.config import Config


def create_repo(config: Config):
    utils.epm([
        'repo',
        'create',
        config.get('repo_path')
    ])


def update_cache():
    utils.epm(['update'])

def update_epm():
    utils.epm(['ei'])


@asynccontextmanager
async def lifespan(app: FastAPI):
    await update_repeat()
    yield


config = Config()
app = FastAPI(lifespan=lifespan, root_path=config.get('root_path'))

update_task_started = False


def update():
    json_file_path = os.path.join(config.get('repo_path'), 'data.json')
    if not os.path.exists(json_file_path):
        with open(json_file_path, 'w') as data_file:
            json.dump({'versions': {}}, data_file, indent=4)
    with open(json_file_path, 'r') as data_file:
        repo_data = json.load(data_file)

    global update_task_started

    if 'last_version_check' in repo_data:
        last_version_check = datetime.datetime.fromisoformat(repo_data['last_version_check'])

        if datetime.datetime.now() - datetime.timedelta(minutes=5) < last_version_check:
            update_task_started = False
            return

    update_cache()
    update_epm()

    providers_path = os.path.join(os.getcwd(), 'autorepacked/providers')
    modules = os.listdir(providers_path)

    versions = repo_data['versions']
    need_update_index = False
    for module_name in modules:
        module = importlib.import_module(f'providers.{module_name}')
        if hasattr(module, 'get_provider'):
            provider = module.get_provider(config)  # type: BaseProvider
            if not provider.disabled:
                name = provider.get_name()
                print(f"request version of {name}")
                version = provider.get_version()
                if name not in versions or versions[name] != version:
                    print(f'{name} has new version {version}')
                    versions[name] = version
                    provider.download()
                    need_update_index = True

    repo_data['versions'] = versions

    current_date = datetime.datetime.utcnow()

    if need_update_index:
        utils.epm(
            args=[
                'repo',
                'index',
                config.get('repo_path'),
            ]
        )
        repo_data['last_index_update'] = current_date.isoformat()

    repo_data['last_version_check'] = current_date.isoformat()

    with open(json_file_path, 'w') as data_file:
        json.dump(repo_data, data_file, indent=4)

    update_task_started = False


@app.post("/update")
def update_method(background_tasks: BackgroundTasks):
    global update_task_started
    if not update_task_started:
        update_task_started = True
        background_tasks.add_task(update)
    return {'status': 'OK'}


@repeat_every(seconds=60 * 60 * 4)
def update_repeat():
    global update_task_started
    if not update_task_started:
        update_task_started = True
        update()


if __name__ == "__main__":
    create_repo(config)
    uvicorn.run(app, host="0.0.0.0", port=8000)
