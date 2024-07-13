from punq import Container, Scope

from infrastructure.repositories.chat.base import BaseChatRepository
from infrastructure.repositories.chat.memory import MemoryChatRepository
from logic.init import _init_container


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(BaseChatRepository, MemoryChatRepository, scope=Scope.singleton)

    return container
