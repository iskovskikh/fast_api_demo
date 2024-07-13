from dataclasses import dataclass
from typing import Any

from domain.entities.chat import Chat, Message
from domain.values.chat import Title, Text
from infrastructure.repositories.chat.base import BaseChatRepository
from infrastructure.repositories.message.base import BaseMessagesRepository
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.chat import ChatWithThatTitleAlreadyExistsException, ChatNotFoundException


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str


@dataclass()
class CreateChatCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    chat_repository: BaseChatRepository

    async def handle(self, command: CreateChatCommand) -> Any:
        if await self.chat_repository.check_chat_exists_by_title(command.title):
            raise ChatWithThatTitleAlreadyExistsException(command.title)

        title = Title(command.title)

        new_chat = Chat.create_chat(title=title)
        await self.chat_repository.add_chat(new_chat)

        return new_chat


@dataclass(frozen=True)
class CreateMessageCommand(BaseCommand):
    text: str
    chat_oid: str


@dataclass()
class CreateMessageCommandHandler(CommandHandler[CreateMessageCommand, Chat]):
    message_repository: BaseMessagesRepository
    chat_repository: BaseChatRepository

    async def handle(self, command: CreateMessageCommand) -> Any:
        chat = await self.chat_repository.get_chat_by_oid(command.chat_oid)

        if not chat:
            raise ChatNotFoundException(chat_oid=command.chat_oid)

        message = Message(text=Text(command.text), chat_oid=command.chat_oid)
        chat.add_message(message)
        await self.message_repository.add_message(message=message)

        return message
