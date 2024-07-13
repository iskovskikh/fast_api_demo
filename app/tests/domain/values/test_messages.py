from uuid import uuid4

import pytest
from faker import Faker

from domain.entities.chat import Chat, Message
from domain.events.chat import NewMessageCreatedEvent
from domain.exceptions.chat import TitleTooLongException, EmptyTextException
from domain.values.chat import Title, Text


def test_create_messages_success(faker: Faker):
    text = Text(faker.text(max_nb_chars=30))
    message = Message(text=text, chat_oid=str(uuid4()))

    assert message.text == text


def test_create_messages_success_long_text(faker: Faker):
    text = Text(faker.text(max_nb_chars=500))
    message = Message(text=text, chat_oid=str(uuid4()))

    assert message.text == text


def test_create_chat_success(faker: Faker):
    title = Title(faker.text(max_nb_chars=12))
    chat = Chat(title=title)

    assert chat.title == title
    assert not chat.messages


def test_create_title_failed(faker: Faker):
    with pytest.raises(EmptyTextException):
        Title('')
    with pytest.raises(TitleTooLongException):
        Title(faker.text(max_nb_chars=300))


def test_add_message_to_chat(faker):
    text = Text(faker.text(max_nb_chars=30))
    message = Message(text=text, chat_oid=str(uuid4()))

    title = Title(faker.text(max_nb_chars=30))
    chat = Chat(title=title)

    chat.add_message(message=message)

    assert message in chat.messages


def test_new_message_events(faker):
    text = Text(faker.text(max_nb_chars=30))
    message = Message(text=text, chat_oid=str(uuid4()))

    title = Title(faker.text(max_nb_chars=30))
    chat = Chat(title=title)

    chat.add_message(message=message)
    events = chat.pull_events()
    pulled_events = chat.pull_events()

    assert not pulled_events, pulled_events
    assert len(events) == 1, events

    new_event = events[0]

    assert isinstance(new_event, NewMessageCreatedEvent), new_event
    assert new_event.message_oid == message.oid
    assert new_event.message_text == message.text.as_generic_type()
    assert new_event.chat_oid == message.chat_oid
