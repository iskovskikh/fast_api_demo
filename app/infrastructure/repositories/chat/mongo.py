from abc import ABC
from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorClient

from domain.entities.chat import Chat
from infrastructure.repositories.chat.base import BaseChatRepository
from infrastructure.repositories.chat.converters import convert_chat_to_document, convert_chat_document_to_entity


@dataclass
class BaseMongoDBRepository(ABC):
    # mongo_db_client: AgnosticClient
    mongo_db_client: AsyncIOMotorClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    @property
    def _collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]


@dataclass
class MongoDBChatRepository(BaseMongoDBRepository, BaseChatRepository):

    async def check_chat_exists_by_title(self, title: str) -> bool:
        return bool(await self._collection.find_one(filter=dict(title=title)))

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        chat_document = await self._collection.find_one(filter=dict(oid=oid))

        if not chat_document:
            return None

        return convert_chat_document_to_entity(chat_document)

    async def add_chat(self, chat: Chat) -> None:
        await self._collection.insert_one(
            convert_chat_to_document(chat)
        )


