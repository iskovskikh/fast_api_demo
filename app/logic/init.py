from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope

from infrastructure.repositories.chat.base import BaseChatRepository
from infrastructure.repositories.message.base import BaseMessagesRepository
from infrastructure.repositories.chat.mongo import MongoDBChatRepository
from infrastructure.repositories.message.mongo import MongoDBMessagesRepository
from logic.commands.chat import CreateChatCommand, CreateChatCommandHandler, CreateMessageCommand, \
    CreateMessageCommandHandler
from logic.mediator import Mediator
from logic.queries.chat import GetChatDetailQueryHandler, GetChatDetailQuery, GetMessagesQuery, GetMessagesQueryHandler
from settings.config import Config


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)
    config: Config = container.resolve(Config)

    def ctrate_mongodb_client():
        return AsyncIOMotorClient(config.mongo_db_connection_uri, serverSelectionTimeoutMS=2000)

    container.register(AsyncIOMotorClient, factory=ctrate_mongodb_client, scope=Scope.singleton)

    client = container.resolve(AsyncIOMotorClient)

    def init_chat_mongodb_repository() -> MongoDBChatRepository:
        return MongoDBChatRepository(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongo_db_chat_collection_name,
        )

    def init_messages_mongodb_repository() -> MongoDBMessagesRepository:
        return MongoDBMessagesRepository(
            mongo_db_client=client,
            mongo_db_db_name=config.mongodb_chat_database,
            mongo_db_collection_name=config.mongo_db_messages_collection_name,
        )

    container.register(BaseChatRepository, factory=init_chat_mongodb_repository, scope=Scope.singleton)
    container.register(BaseMessagesRepository, factory=init_messages_mongodb_repository, scope=Scope.singleton)

    # command handlers
    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)

    # query handlers
    container.register(GetChatDetailQueryHandler)
    container.register(GetMessagesQueryHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand,
            [container.resolve(CreateChatCommandHandler)]
        )
        mediator.register_command(
            CreateMessageCommand,
            [container.resolve(CreateMessageCommandHandler)]
        )
        mediator.register_query(
            query=GetChatDetailQuery,
            query_handler=container.resolve(GetChatDetailQueryHandler)
        )
        mediator.register_query(
            query=GetMessagesQuery,
            query_handler=container.resolve(GetMessagesQueryHandler)
        )
        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
