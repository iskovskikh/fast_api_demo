from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.events.chat import NewChatCreatedEvent, NewMessageCreatedEvent
from domain.values.chat import Title, Text


@dataclass(eq=False)
class Message(BaseEntity):
    chat_oid: str
    text: Text


@dataclass(eq=False)
class Chat(BaseEntity):
    title: Title
    messages: set[Message] = field(
        default_factory=set,
        kw_only=True
    )

    @classmethod
    def create_chat(cls, title: Title) -> 'Chat':
        new_chat = cls(title=title)
        new_chat.register_event(NewChatCreatedEvent(oid=new_chat.oid, title=new_chat.title.as_generic_type()))
        return new_chat

    def add_message(self, message: Message):
        self.messages.add(message)
        self.register_event(
            NewMessageCreatedEvent(
                message_text=message.text.as_generic_type(),
                message_oid=message.oid,
                chat_oid=message.chat_oid,
            )
        )
