from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.entities import User, Post, Comment

class IUserRepository(ABC):
    @abstractmethod
    def create(self, user: 'User'): pass
    
    @abstractmethod
    def get_all(self) -> List['User']: pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> 'User': pass
    
    @abstractmethod
    def delete(self, user_id: int): pass

class IPostRepository(ABC):
    @abstractmethod
    def create(self, post: 'Post'): pass
    
    @abstractmethod
    def get_all(self) -> List['Post']: pass
    
    @abstractmethod
    def get_by_id(self, post_id: int) -> 'Post': pass
    
    @abstractmethod
    def delete(self, post_id: int): pass

class ICommentRepository(ABC):
    @abstractmethod
    def create(self, comment: 'Comment'): pass
    
    @abstractmethod
    def get_all(self) -> List['Comment']: pass
    
    @abstractmethod
    def get_by_id(self, comment_id: int) -> 'Comment': pass
    
    @abstractmethod
    def delete(self, comment_id: int): pass