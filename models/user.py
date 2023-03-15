from models.base import BaseModel
from models.task import Task
from typing import List
import datetime
import codecs
import os
import re

date_regexp = r'[0-9]{1,2}-[0-9]{1,2}-[0-9]{4} [0-9]{2}:[0-9]{2}'
date_re = re.compile(date_regexp)


class Geo(BaseModel):
    lat: str
    lng: str


class Address(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo


class Company(BaseModel):
    name: str
    catchPhrase: str
    bs: str


class User(BaseModel):
    name: str
    username: str
    email: str
    address: Address
    phone: str
    website: str
    company: Company
    _tasks: List[Task]

    def add_task(self, task: Task):
        if self._tasks is None:
            self._tasks = list()
        self._tasks.append(task)

    @property
    def tasks(self) -> List[Task]:
        return self._tasks if self._tasks else list()

    @property
    def completed_tasks(self) -> List[Task]:
        return [task for task in self._tasks if task.completed]

    @property
    def opened_tasks(self) -> List[Task]:
        return [task for task in self._tasks if not task.completed]

    def archiving_file(self, file_dir, file_path: str):
        with codecs.open(file_path, 'r', 'utf-8') as file:
            text = file.read()
        date = date_re.search(text)
        if date:
            date_name = date.group(0).replace(' ', 'T').replace(':', '-')
            new_file = os.path.join(
                file_dir,
                f'old_{self.username}_{date_name}.txt',
            )
            with codecs.open(new_file, 'w', 'utf-8') as file:
                file.write(text, )

    def create_file(self, file_dir: str, file_template: str):
        file_path = os.path.join(
            file_dir,
            f'{self.username}.txt'
        )
        if os.path.exists(file_path):
            self.archiving_file(file_dir, file_path)

        completed_tasks = self.completed_tasks
        opened_tasks = self.opened_tasks

        text = file_template.format(
            company_name=self.company.name,
            name=self.name,
            email=self.email,
            date_now=datetime.datetime.now().strftime('%d-%m-%Y %H:%M'),
            all_tasks_count=len(self.tasks),
            opened_tasks_count=len(opened_tasks),
            completed_tasks_count=len(completed_tasks),
            opened_tasks='\n'.join([task.title_for_file for task in opened_tasks]),
            completed_tasks='\n'.join([task.title_for_file for task in completed_tasks]),
        )
        with codecs.open(file_path, 'w', 'utf-8') as file:
            file.write(text )

        return file_path
