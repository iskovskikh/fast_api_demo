from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    mongo_db_connection_uri: str = Field(alias='MONGO_DB_CONNECTION_URI')
    mongodb_chat_database: str = Field(default='chat', alias='MONGO_DB_CHAT_DATABASE')
    mongo_db_chat_collection_name: str = Field(default='chat', alias='MONGO_DB_CHAT_COLLECTION')
    mongo_db_messages_collection_name: str = Field(default='messages', alias='MONGO_DB_MESSAGES_COLLECTION')
