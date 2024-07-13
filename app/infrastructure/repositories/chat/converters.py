from typing import Mapping, Any

from domain.entities.chat import Chat, Message
from domain.values.chat import Text, Title


def convert_message_entity_to_document(message: Message) -> dict:
    return dict(
        oid=message.oid,
        text=message.text.as_generic_type(),
        chat_oid=message.chat_oid
    )


def convert_message_document_to_entity(message_document: Mapping[str, Any]) -> Message:
    return Message(
        oid=message_document['oid'],
        text=Text(value=message_document['text']),
        chat_oid=message_document['chat_oid']
    )


def convert_chat_to_document(chat: Chat) -> dict:
    return dict(
        oid=chat.oid,
        title=chat.title.as_generic_type(),
        # messages=[convert_message_to_document(message) for message in chat.messages]
    )


def convert_chat_document_to_entity(chat_document: Mapping[str, Any]):
    return Chat(
        title=Title(value=chat_document['title']),
        oid=chat_document['oid'],
        # messages={
        #     convert_message_document_to_entity(message_document) for message_document in chat_document['messages']
        # }
    )
