from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass(frozen=True)
class NewChatCreatedEvent(BaseEvent):
    oid: str
    title: str


@dataclass(frozen=True)
class NewMessageCreatedEvent(BaseEvent):
    message_text: str
    message_oid: str
    chat_oid: str
