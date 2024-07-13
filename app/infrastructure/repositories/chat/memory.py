from dataclasses import dataclass, field

from domain.entities.chat import Chat
from infrastructure.repositories.chat.base import BaseChatRepository


@dataclass
class MemoryChatRepository(BaseChatRepository):
    _saved_chat_list: list[Chat] = field(default_factory=dict, kw_only=True)

    async def add_chat(self, chat: Chat) -> None:
        self._saved_chat_list.append(chat)

    async def check_chat_exists_by_title(self, title: str) -> bool:
        try:
            return bool(next(
                chat for chat in self._saved_chat_list if chat.title.as_generic_type() == title
            ))
        except StopIteration:
            return False

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        try:
            return next(
                chat for chat in self._saved_chat_list if chat.oid == oid
            )
        except StopIteration:
            return None