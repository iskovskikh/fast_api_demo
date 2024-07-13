from dataclasses import dataclass
from typing import Iterable

from domain.entities.chat import Message
from infrastructure.repositories.chat.converters import convert_message_entity_to_document, convert_message_document_to_entity
from infrastructure.repositories.chat.mongo import BaseMongoDBRepository
from infrastructure.repositories.filters.messages import GetMessagesFilters
from infrastructure.repositories.message.base import BaseMessagesRepository


@dataclass
class MongoDBMessagesRepository(BaseMongoDBRepository, BaseMessagesRepository):

    async def add_message(self, message: Message) -> None:
        await self._collection.insert_one(
            convert_message_entity_to_document(message)
        )

    async def get_messages(self, chat_oid: str, filters: GetMessagesFilters) -> tuple[Iterable[Message], int]:
        find = {'chat_oid': chat_oid}
        cursor = self._collection.find(filter=find).skip(filters.offset).limit(filters.limit)
        count = await self._collection.count_documents(filter=find)

        messages = [
            convert_message_document_to_entity(message_document=message_document)
            async for message_document in cursor
        ]

        return messages, count
