from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.entities import User, Post, Comment


class IUserRepository(ABC):
    """Интерфейс репозитория для работы с пользователями."""
    
    @abstractmethod
    def create(self, user: 'User') -> 'User':
        """Создать нового пользователя."""
        pass
    
    @abstractmethod
    def get_all(self) -> List['User']:
        """Получить всех пользователей."""
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional['User']:
        """Получить пользователя по ID."""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> None:
        """Удалить пользователя по ID."""
        pass


class IPostRepository(ABC):
    """Интерфейс репозитория для работы с публикациями."""
    
    @abstractmethod
    def create(self, post: 'Post') -> 'Post':
        """Создать новую публикацию."""
        pass
    
    @abstractmethod
    def get_all(self) -> List['Post']:
        """Получить все публикации."""
        pass
    
    @abstractmethod
    def get_by_id(self, post_id: int) -> Optional['Post']:
        """Получить публикацию по ID."""
        pass
    
    @abstractmethod
    def delete(self, post_id: int) -> None:
        """Удалить публикацию по ID."""
        pass


class ICommentRepository(ABC):
    """Интерфейс репозитория для работы с комментариями."""
    
    @abstractmethod
    def create(self, comment: 'Comment') -> 'Comment':
        """Создать новый комментарий."""
        pass
    
    @abstractmethod
    def get_all(self) -> List['Comment']:
        """Получить все комментарии."""
        pass
    
    @abstractmethod
    def get_by_id(self, comment_id: int) -> Optional['Comment']:
        """Получить комментарий по ID."""
        pass
    
    @abstractmethod
    def delete(self, comment_id: int) -> None:
        """Удалить комментарий по ID."""
        pass