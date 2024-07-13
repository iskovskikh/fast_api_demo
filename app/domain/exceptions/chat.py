from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class EmptyTextException(ApplicationException):
    @property
    def message(self):
        return f'Не может быть пустым'


@dataclass(frozen=True, eq=False)
class TitleTooLongException(ApplicationException):
    title: str

    @property
    def message(self):
        return f'Название "{self.title}" слишком большое"'
