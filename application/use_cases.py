from domain.entities import User, Post, Comment
from domain.factories import UserFactory, PostFactory, CommentFactory
from domain.repositories import IUserRepository, IPostRepository, ICommentRepository


class CreateUserUseCase:
    """Сценарий создания нового пользователя."""
    
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo
    
    def execute(self, username: str, email: str) -> User:
        """
        Создать нового пользователя.
        
        Args:
            username: Имя пользователя
            email: Электронная почта
            
        Returns:
            Созданный объект пользователя
        """
        user = UserFactory.create(username, email)
        return self.user_repo.create(user)


class CreatePostUseCase:
    """Сценарий создания новой публикации."""
    
    def __init__(self, post_repo: IPostRepository, user_repo: IUserRepository):
        self.post_repo = post_repo
        self.user_repo = user_repo
    
    def execute(self, title: str, content: str, author_id: int) -> Post:
        """
        Создать новую публикацию.
        
        Args:
            title: Заголовок публикации
            content: Содержание публикации
            author_id: ID автора
            
        Returns:
            Созданный объект публикации
            
        Raises:
            ValueError: Если автор не существует
        """
        author = self.user_repo.get_by_id(author_id)
        if not author:
            raise ValueError(f"Автор с ID {author_id} не существует")
        
        post = PostFactory.create(title, content, author_id)
        return self.post_repo.create(post)


class CreateCommentUseCase:
    """Сценарий создания нового комментария."""
    
    def __init__(self, 
                 comment_repo: ICommentRepository, 
                 post_repo: IPostRepository,
                 user_repo: IUserRepository):
        self.comment_repo = comment_repo
        self.post_repo = post_repo
        self.user_repo = user_repo
    
    def execute(self, content: str, post_id: int, author_id: int) -> Comment:
        """
        Создать новый комментарий.
        
        Args:
            content: Содержание комментария
            post_id: ID публикации
            author_id: ID автора
            
        Returns:
            Созданный объект комментария
            
        Raises:
            ValueError: Если публикация или автор не существуют
        """
        if not self.post_repo.get_by_id(post_id):
            raise ValueError(f"Публикация с ID {post_id} не существует")
        if not self.user_repo.get_by_id(author_id):
            raise ValueError(f"Автор с ID {author_id} не существует")
        
        comment = CommentFactory.create(content, post_id, author_id)
        return self.comment_repo.create(comment)


class GetPostUseCase:
    """Сценарий получения публикации по ID."""
    
    def __init__(self, post_repo: IPostRepository):
        self.post_repo = post_repo
    
    def execute(self, post_id: int) -> Post | None:
        """
        Получить публикацию по ID.
        
        Args:
            post_id: ID публикации
            
        Returns:
            Объект публикации или None если не найдена
        """
        return self.post_repo.get_by_id(post_id)


class GetAllUsersUseCase:
    """Сценарий получения всех пользователей."""
    
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo
    
    def execute(self) -> list[User]:
        """Получить всех пользователей."""
        return self.user_repo.get_all()


class GetUserByIdUseCase:
    """Сценарий получения пользователя по ID."""
    
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo
    
    def execute(self, user_id: int) -> User | None:
        """
        Получить пользователя по ID.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Объект пользователя или None если не найден
        """
        return self.user_repo.get_by_id(user_id)


class DeleteUserUseCase:
    """Сценарий удаления пользователя."""
    
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo
    
    def execute(self, user_id: int) -> None:
        """
        Удалить пользователя по ID.
        
        Args:
            user_id: ID пользователя для удаления
        """
        return self.user_repo.delete(user_id)


class GetAllPostsUseCase:
    """Сценарий получения всех публикаций."""
    
    def __init__(self, post_repo: IPostRepository):
        self.post_repo = post_repo
    
    def execute(self) -> list[Post]:
        """Получить все публикации."""
        return self.post_repo.get_all()


class DeletePostUseCase:
    """Сценарий удаления публикации."""
    
    def __init__(self, post_repo: IPostRepository):
        self.post_repo = post_repo
    
    def execute(self, post_id: int) -> None:
        """
        Удалить публикацию по ID.
        
        Args:
            post_id: ID публикации для удаления
        """
        return self.post_repo.delete(post_id)


class GetAllCommentsUseCase:
    """Сценарий получения всех комментариев."""
    
    def __init__(self, comment_repo: ICommentRepository):
        self.comment_repo = comment_repo
    
    def execute(self) -> list[Comment]:
        """Получить все комментарии."""
        return self.comment_repo.get_all()


class GetCommentByIdUseCase:
    """Сценарий получения комментария по ID."""
    
    def __init__(self, comment_repo: ICommentRepository):
        self.comment_repo = comment_repo
    
    def execute(self, comment_id: int) -> Comment | None:
        """
        Получить комментарий по ID.
        
        Args:
            comment_id: ID комментария
            
        Returns:
            Объект комментария или None если не найден
        """
        return self.comment_repo.get_by_id(comment_id)


class DeleteCommentUseCase:
    """Сценарий удаления комментария."""
    
    def __init__(self, comment_repo: ICommentRepository):
        self.comment_repo = comment_repo
    
    def execute(self, comment_id: int) -> None:
        """
        Удалить комментарий по ID.
        
        Args:
            comment_id: ID комментария для удаления
        """
        return self.comment_repo.delete(comment_id)