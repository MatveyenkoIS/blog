from infrastructure.repositories import SQLUserRepository, SQLPostRepository, SQLCommentRepository
from domain.repositories import IUserRepository, IPostRepository, ICommentRepository

class RepositoryFactory:
    
    def create_user_repository(self) -> IUserRepository:
        return SQLUserRepository()
    
    def create_post_repository(self) -> IPostRepository:
        return SQLPostRepository()
    
    def create_comment_repository(self) -> ICommentRepository:
        return SQLCommentRepository()


class DatabaseFactory:
    
    @staticmethod
    def initialize_db(app):
        from infrastructure.database import db
        db.init_app(app)
        with app.app_context():
            db.create_all()