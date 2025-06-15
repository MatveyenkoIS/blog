from domain.entities import User, Post, Comment

class UserFactory:
    @staticmethod
    def create(username, email):
        return User(id=None, username=username, email=email)

class PostFactory:
    @staticmethod
    def create(title, content, author_id):
        return Post(id=None, title=title, content=content, author_id=author_id)

class CommentFactory:
    @staticmethod
    def create(content, post_id, author_id):
        return Comment(id=None, content=content, post_id=post_id, author_id=author_id)