from typing import Iterable

from pydantic import BaseModel

from application.api.schemas import BaseQueryResponseSchema
from domain.entities.chat import Chat, Message


class CreateChatRequestSchema(BaseModel):
    title: str


class CreateChatResponseSchema(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> 'CreateChatResponseSchema':
        return cls(
            oid=chat.oid,
            title=chat.title.as_generic_type()
        )


class CreateMessageSchema(BaseModel):
    text: str


class CreateMessageResponseSchema(BaseModel):
    text: str
    oid: str

    @classmethod
    def from_entity(cls, message: Message) -> 'CreateMessageResponseSchema':
        return CreateMessageResponseSchema(
            oid=message.oid,
            text=message.text.as_generic_type()
        )


class MessageDetailSchema(BaseModel):
    oid: str
    text: str

    @classmethod
    def from_entity(cls, message: Message) -> 'MessageDetailSchema':
        return cls(
            oid=message.oid,
            text=message.text.as_generic_type()
        )


class ChatDetailSchema(BaseModel):
    oid: str
    title: str
    messages: Iterable[MessageDetailSchema]

    @classmethod
    def from_entity(cls, chat: Chat) -> 'ChatDetailSchema':
        return cls(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
            messages=[MessageDetailSchema.from_entity(message) for message in chat.messages]
        )


class GetMessagesQueryResponseSchema(BaseQueryResponseSchema):
    items: MessageDetailSchema
