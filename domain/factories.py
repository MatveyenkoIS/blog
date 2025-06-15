from domain.entities import User, Post, Comment


class UserFactory:
    """Фабрика для создания объектов пользователей."""
    
    @staticmethod
    def create(username: str, email: str) -> User:
        """
        Создать нового пользователя.
        
        Args:
            username: Имя пользователя
            email: Электронная почта
            
        Returns:
            Объект пользователя без ID
        """
        return User(id=None, username=username, email=email)


class PostFactory:
    """Фабрика для создания объектов публикаций."""
    
    @staticmethod
    def create(title: str, content: str, author_id: int) -> Post:
        """
        Создать новую публикацию.
        
        Args:
            title: Заголовок
            content: Содержание
            author_id: ID автора
            
        Returns:
            Объект публикации без ID
        """
        return Post(id=None, title=title, content=content, author_id=author_id)


class CommentFactory:
    """Фабрика для создания объектов комментариев."""
    
    @staticmethod
    def create(content: str, post_id: int, author_id: int) -> Comment:
        """
        Создать новый комментарий.
        
        Args:
            content: Содержание
            post_id: ID публикации
            author_id: ID автора
            
        Returns:
            Объект комментария без ID
        """
        return Comment(id=None, content=content, post_id=post_id, author_id=author_id)