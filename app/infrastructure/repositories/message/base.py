from abc import abstractmethod
from dataclasses import dataclass
from typing import Iterable

from domain.entities.chat import Message
from infrastructure.repositories.filters.messages import GetMessagesFilters


@dataclass
class BaseMessagesRepository:
    @abstractmethod
    async def add_message(self, message: Message) -> None:
        ...

    @abstractmethod
    async def get_messages(self, chat_oid: str, filters: GetMessagesFilters) -> tuple[Iterable[Message], int]:
        ...
