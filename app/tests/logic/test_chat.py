import pytest
from faker import Faker

from domain.entities.chat import Chat
from domain.values.chat import Title
from infrastructure.repositories.chat.base import BaseChatRepository
from infrastructure.repositories.chat.memory import MemoryChatRepository
from logic.commands.chat import CreateChatCommand
from logic.exceptions.chat import ChatWithThatTitleAlreadyExistsException
from logic.mediator import Mediator


@pytest.mark.asyncio
async def test_create_chat_command_success(
        chat_repository,
        mediator: Mediator,
        faker: Faker
):
    chat: Chat
    chat, *_ = await mediator.handle_command(
        CreateChatCommand(title=faker.text(max_nb_chars=30))
    )

    assert await chat_repository.check_chat_exists_by_title(chat.title.as_generic_type())


@pytest.mark.asyncio
async def test_create_chat_command_title_exists(
        chat_repository,
        mediator: Mediator,
        faker: Faker
):
    title_text = faker.text(max_nb_chars=30)
    chat = Chat.create_chat(title=Title(title_text))
    await chat_repository.add_chat(chat)

    assert chat in chat_repository._saved_chat_list

    with pytest.raises(ChatWithThatTitleAlreadyExistsException):
        await mediator.handle_command(CreateChatCommand(title=title_text))

    assert len(chat_repository._saved_chat_list) == 1
