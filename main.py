from api import get_users
from pathlib import Path
import traceback
import logging
import os

logger = logging.getLogger()

BASE_DIR = Path(__file__).resolve().parent


def path_dir(name_dir: str) -> str:
    tasks_dir = os.path.join(
        BASE_DIR,
        name_dir
    )
    if not os.path.exists(tasks_dir):
        os.makedirs(tasks_dir)
    return tasks_dir


def get_template() -> str:
    template = """# Отчёт для {company_name}.
{name} <{email}> {date_now}
Всего задач: {all_tasks_count}

## Актуальные задачи ({opened_tasks_count}):
{opened_tasks}

## Завершённые задачи ({completed_tasks_count}):
{completed_tasks}"""
    return template


def main():
    users = get_users()

    tasks_dir = path_dir('tasks')

    template = get_template()

    for pk, user in users.items():
        try:
            user.create_file(tasks_dir, template)
        except Exception:
            continue


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.error(traceback.format_exc())
