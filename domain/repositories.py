from abc import ABC, abstractmethod

class IUserRepository(ABC):
    @abstractmethod
    def create(self, user): pass

    @abstractmethod
    def get_by_id(self, user_id): pass

class IPostRepository(ABC):
    @abstractmethod
    def create(self, post): pass

    @abstractmethod
    def get_by_id(self, post_id): pass

class ICommentRepository(ABC):
    @abstractmethod
    def create(self, comment): pass