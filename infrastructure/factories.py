from infrastructure.repositories import SQLUserRepository, SQLPostRepository, SQLCommentRepository
from domain.repositories import IUserRepository, IPostRepository, ICommentRepository


class RepositoryFactory:
    """Фабрика для создания репозиториев."""
    
    def create_user_repository(self) -> IUserRepository:
        """Создать репозиторий пользователей."""
        return SQLUserRepository()
    
    def create_post_repository(self) -> IPostRepository:
        """Создать репозиторий публикаций."""
        return SQLPostRepository()
    
    def create_comment_repository(self) -> ICommentRepository:
        """Создать репозиторий комментариев."""
        return SQLCommentRepository()


class DatabaseFactory:
    """Фабрика для работы с базой данных."""
    
    @staticmethod
    def initialize_db(app) -> None:
        """
        Инициализировать базу данных.
        
        Args:
            app: Экземпляр Flask приложения
        """
        from infrastructure.database import db
        db.init_app(app)
        with app.app_context():
            db.create_all()