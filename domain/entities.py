class User:
    """Сущность пользователя."""
    
    def __init__(self, id: int, username: str, email: str):
        """
        Инициализация пользователя.
        
        Args:
            id: Уникальный идентификатор
            username: Имя пользователя
            email: Электронная почта
        """
        self.id = id
        self.username = username
        self.email = email


class Post:
    """Сущность публикации."""
    
    def __init__(self, id: int, title: str, content: str, author_id: int):
        """
        Инициализация публикации.
        
        Args:
            id: Уникальный идентификатор
            title: Заголовок
            content: Содержание
            author_id: ID автора
        """
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id


class Comment:
    """Сущность комментария."""
    
    def __init__(self, id: int, content: str, post_id: int, author_id: int):
        """
        Инициализация комментария.
        
        Args:
            id: Уникальный идентификатор
            content: Содержание
            post_id: ID публикации
            author_id: ID автора
        """
        self.id = id
        self.content = content
        self.post_id = post_id
        self.author_id = author_id