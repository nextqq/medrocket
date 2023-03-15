from models.base import BaseModel


class Task(BaseModel):
    id: int
    title: str
    completed: bool

    @property
    def title_for_file(self):
        return f'- {self.title}' if len(self.title) <= 46 else f'- {self.title[0:45]}...'
