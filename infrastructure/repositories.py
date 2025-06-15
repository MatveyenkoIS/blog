from domain.entities import User, Post, Comment
from domain.repositories import IUserRepository, IPostRepository, ICommentRepository
from infrastructure.database import db, UserModel, PostModel, CommentModel


class SQLUserRepository(IUserRepository):
    """Реализация репозитория пользователей на SQLAlchemy."""
    
    def create(self, user: User) -> User:
        """
        Создать нового пользователя в базе данных.
        
        Args:
            user: Сущность пользователя
            
        Returns:
            Созданная сущность пользователя с ID
        """
        user_model = UserModel(username=user.username, email=user.email)
        db.session.add(user_model)
        db.session.commit()
        return User(
            id=user_model.id, 
            username=user_model.username, 
            email=user_model.email
        )
    
    def get_by_id(self, user_id: int) -> User | None:
        """
        Получить пользователя по ID.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Сущность пользователя или None если не найден
        """
        user_model = db.session.get(UserModel, user_id)
        if user_model:
            return User(
                id=user_model.id,
                username=user_model.username,
                email=user_model.email
            )
        return None
    
    def get_all(self) -> list[User]:
        """Получить всех пользователей."""
        users = UserModel.query.all()
        return [
            User(id=u.id, username=u.username, email=u.email) 
            for u in users
        ]
    
    def delete(self, user_id: int) -> None:
        """
        Удалить пользователя по ID.
        
        Args:
            user_id: ID пользователя для удаления
        """
        user = UserModel.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()


class SQLPostRepository(IPostRepository):
    """Реализация репозитория публикаций на SQLAlchemy."""
    
    def create(self, post: Post) -> Post:
        """
        Создать новую публикацию в базе данных.
        
        Args:
            post: Сущность публикации
            
        Returns:
            Созданная сущность публикации с ID
        """
        post_model = PostModel(
            title=post.title,
            content=post.content,
            author_id=post.author_id
        )
        db.session.add(post_model)
        db.session.commit()
        return Post(
            id=post_model.id,
            title=post_model.title,
            content=post_model.content,
            author_id=post_model.author_id
        )
    
    def get_by_id(self, post_id: int) -> Post | None:
        """
        Получить публикацию по ID.
        
        Args:
            post_id: ID публикации
            
        Returns:
            Сущность публикации или None если не найдена
        """
        post_model = db.session.get(PostModel, post_id)
        if post_model:
            return Post(
                id=post_model.id,
                title=post_model.title,
                content=post_model.content,
                author_id=post_model.author_id
            )
        return None
    
    def get_all(self) -> list[Post]:
        """Получить все публикации."""
        posts = PostModel.query.all()
        return [
            Post(id=p.id, title=p.title, content=p.content, author_id=p.author_id) 
            for p in posts
        ]

    def delete(self, post_id: int) -> None:
        """
        Удалить публикацию по ID.
        
        Args:
            post_id: ID публикации для удаления
        """
        post = PostModel.query.get(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()


class SQLCommentRepository(ICommentRepository):
    """Реализация репозитория комментариев на SQLAlchemy."""
    
    def create(self, comment: Comment) -> Comment:
        """
        Создать новый комментарий в базе данных.
        
        Args:
            comment: Сущность комментария
            
        Returns:
            Созданная сущность комментария с ID
        """
        comment_model = CommentModel(
            content=comment.content,
            post_id=comment.post_id,
            author_id=comment.author_id
        )
        db.session.add(comment_model)
        db.session.commit()
        return Comment(
            id=comment_model.id,
            content=comment_model.content,
            post_id=comment_model.post_id,
            author_id=comment_model.author_id
        )
    
    def get_all(self) -> list[Comment]:
        """Получить все комментарии."""
        comments = CommentModel.query.all()
        return [
            Comment(
                id=c.id,
                content=c.content,
                post_id=c.post_id,
                author_id=c.author_id
            ) for c in comments
        ]

    def get_by_id(self, comment_id: int) -> Comment | None:
        """
        Получить комментарий по ID.
        
        Args:
            comment_id: ID комментария
            
        Returns:
            Сущность комментария или None если не найден
        """
        comment = CommentModel.query.get(comment_id)
        if comment:
            return Comment(
                id=comment.id,
                content=comment.content,
                post_id=comment.post_id,
                author_id=comment.author_id
            )
        return None

    def delete(self, comment_id: int) -> None:
        """
        Удалить комментарий по ID.
        
        Args:
            comment_id: ID комментария для удаления
        """
        comment = CommentModel.query.get(comment_id)
        if comment:
            db.session.delete(comment)
            db.session.commit()