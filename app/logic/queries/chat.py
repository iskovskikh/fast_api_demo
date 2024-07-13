from dataclasses import dataclass
from typing import Generic, Iterable

from domain.entities.chat import Chat, Message
from infrastructure.repositories.chat.base import BaseChatRepository
from infrastructure.repositories.message.base import BaseMessagesRepository
from infrastructure.repositories.filters.messages import GetMessagesFilters
from logic.exceptions.chat import ChatNotFoundException
from logic.queries.base import BaseQuery, BaseQueryHandler, QT, QR


@dataclass(frozen=True)
class GetChatDetailQuery(BaseQuery):
    chat_oid: str


@dataclass(frozen=True)
class GetMessagesQuery(BaseQuery):
    chat_oid: str
    filters: GetMessagesFilters


@dataclass(frozen=True)
class GetChatDetailQueryHandler(BaseQueryHandler, Generic[QT, QR]):
    chat_repository: BaseChatRepository
    messages_repository: BaseMessagesRepository

    async def handle(self, query: GetChatDetailQuery) -> Chat:
        chat = await self.chat_repository.get_chat_by_oid(query.chat_oid)

        if not chat:
            raise ChatNotFoundException(chat_oid=query.chat_oid)

        return chat


@dataclass(frozen=True)
class GetMessagesQueryHandler(BaseQueryHandler):
    messages_repository: BaseMessagesRepository

    async def handle(self, query: GetMessagesQuery) -> Iterable[Message]:
        return await self.messages_repository.get_messages(
            chat_oid=query.chat_oid,
            filters=query.filters
        )
