from domain.entities import User, Post, Comment
from domain.factories import UserFactory, PostFactory, CommentFactory
from domain.repositories import IUserRepository, IPostRepository, ICommentRepository


class CreateUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo
    
    def execute(self, username, email):
        user = UserFactory.create(username, email)
        return self.user_repo.create(user)


class CreatePostUseCase:
    def __init__(self, post_repo: IPostRepository, user_repo: IUserRepository):
        self.post_repo = post_repo
        self.user_repo = user_repo
    
    def execute(self, title, content, author_id):
        author = self.user_repo.get_by_id(author_id)
        if not author:
            raise ValueError(f"Author with ID {author_id} does not exist")
        
        post = PostFactory.create(title, content, author_id)
        return self.post_repo.create(post)


class CreateCommentUseCase:
    def __init__(self, comment_repo: ICommentRepository, 
                 post_repo: IPostRepository,
                 user_repo: IUserRepository):
        self.comment_repo = comment_repo
        self.post_repo = post_repo
        self.user_repo = user_repo
    
    def execute(self, content, post_id, author_id):
        if not self.post_repo.get_by_id(post_id):
            raise ValueError(f"Post with ID {post_id} does not exist")
        if not self.user_repo.get_by_id(author_id):
            raise ValueError(f"Author with ID {author_id} does not exist")
        
        comment = CommentFactory.create(content, post_id, author_id)
        return self.comment_repo.create(comment)


class GetPostUseCase:
    def __init__(self, post_repo: IPostRepository):
        self.post_repo = post_repo
    
    def execute(self, post_id):
        return self.post_repo.get_by_id(post_id)