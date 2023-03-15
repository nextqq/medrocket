from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from collections import defaultdict
from models.task import Task
from models.user import User
import requests
import logging

retries = Retry(total=3, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
logger = logging.getLogger()


def get_response(session: requests.Session, url) -> dict:
    response = session.get(
        url=url,
    )
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        logger.error('Ошибка загрузки {url} - {code}'.format(
            url=url,
            code=response.status_code,
        ))


def download_users_and_tasks():
    with requests.Session() as session:
        session.mount('https://', HTTPAdapter(max_retries=retries))
        users = get_response(
            session,
            'https://json.medrocket.ru/users'
        )
        if len(users):
            tasks = get_response(
                session,
                'https://json.medrocket.ru/todos'
            )
            if len(tasks):
                return users, tasks


def get_users() -> dict:
    users_list, tasks_list = download_users_and_tasks()
    users = defaultdict(User)
    if users_list and tasks_list:
        users = defaultdict(User)
        for user in users_list:
            users[str(user['id'])].create(user)

        for item in tasks_list:
            task = Task()
            task.create(item)
            if 'userId' in item:
                users[str(item['userId'])].add_task(task)

    return users
