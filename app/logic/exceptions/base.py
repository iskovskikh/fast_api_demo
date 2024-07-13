from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class LogicException(ApplicationException):
    @property
    def message(self):
        return f'В обработке запроса возникла ошибка'
