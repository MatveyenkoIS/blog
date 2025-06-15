from domain.entities import User, Post, Comment
from domain.repositories import IUserRepository, IPostRepository, ICommentRepository
from infrastructure.database import db, UserModel, PostModel, CommentModel


class SQLUserRepository(IUserRepository):
    def create(self, user: User):
        user_model = UserModel(username=user.username, email=user.email)
        db.session.add(user_model)
        db.session.commit()
        return User(
            id=user_model.id, 
            username=user_model.username, 
            email=user_model.email
        )
    
    def get_by_id(self, user_id):
        user_model = db.session.get(UserModel, user_id)
        if user_model:
            return User(
                id=user_model.id,
                username=user_model.username,
                email=user_model.email
            )


class SQLPostRepository(IPostRepository):
    def create(self, post: Post):
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
    
    def get_by_id(self, post_id):
        post_model = db.session.get(PostModel, post_id)
        if post_model:
            return Post(
                id=post_model.id,
                title=post_model.title,
                content=post_model.content,
                author_id=post_model.author_id
            )


class SQLCommentRepository(ICommentRepository):
    def create(self, comment: Comment):
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