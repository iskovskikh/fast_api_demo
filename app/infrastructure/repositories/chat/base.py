from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.chat import Chat


@dataclass
class BaseChatRepository(ABC):

    @abstractmethod
    async def add_chat(self, chat: Chat) -> None:
        ...

    @abstractmethod
    async def check_chat_exists_by_title(self, title: str) -> bool:
        ...

    @abstractmethod
    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        ...


