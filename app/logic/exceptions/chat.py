from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(frozen=True, eq=False)
class ChatNotFoundException(LogicException):
    chat_oid: str

    @property
    def message(self):
        return f'chat "{self.chat_oid}" не существует'


@dataclass(frozen=True, eq=False)
class ChatWithThatTitleAlreadyExistsException(LogicException):
    title: str

    @property
    def message(self):
        return f'chat с именем "{self.title}" уже существует'
