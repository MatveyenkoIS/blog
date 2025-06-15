import pytest
from unittest.mock import MagicMock
from domain.entities import User, Post, Comment
from application.use_cases import (
    CreateUserUseCase, 
    CreatePostUseCase, 
    CreateCommentUseCase,
    GetPostUseCase
)
from infrastructure.database import db, UserModel, PostModel, CommentModel
from interfaces.web.app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


class TestUseCases:
    def test_create_user(self):
        mock_repo = MagicMock()
        mock_repo.create.return_value = User(1, "test", "test@example.com")
        
        use_case = CreateUserUseCase(mock_repo)
        user = use_case.execute("test", "test@example.com")
        
        assert user.id == 1
        assert user.username == "test"
        mock_repo.create.assert_called_once()

    def test_create_post(self):
        mock_post_repo = MagicMock()
        mock_user_repo = MagicMock()
        
        mock_user = User(1, "test_user", "test@example.com")
        mock_user_repo.get_by_id.return_value = mock_user
        
        mock_post_repo.create.return_value = Post(1, "Title", "Content", 1)
        
        use_case = CreatePostUseCase(mock_post_repo, mock_user_repo)
        post = use_case.execute("Title", "Content", 1)
        
        assert post.id == 1
        assert post.title == "Title"
        mock_post_repo.create.assert_called_once()
        mock_user_repo.get_by_id.assert_called_once_with(1)

    def test_get_post_found(self):
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = Post(1, "Title", "Content", 1)
        
        use_case = GetPostUseCase(mock_repo)
        post = use_case.execute(1)
        
        assert post.id == 1
        mock_repo.get_by_id.assert_called_once_with(1)

    def test_get_post_not_found(self):
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = None
        
        use_case = GetPostUseCase(mock_repo)
        post = use_case.execute(999)
        
        assert post is None
    
    def test_create_comment(self):
        mock_comment_repo = MagicMock()
        mock_post_repo = MagicMock()
        mock_user_repo = MagicMock()
        
        mock_post = Post(1, "Title", "Content", 1)
        mock_user = User(1, "test", "test@example.com")
        mock_comment = Comment(1, "Nice", 1, 1)
        
        mock_post_repo.get_by_id.return_value = mock_post
        mock_user_repo.get_by_id.return_value = mock_user
        mock_comment_repo.create.return_value = mock_comment
        
        use_case = CreateCommentUseCase(
            mock_comment_repo, 
            mock_post_repo,
            mock_user_repo
        )
        
        comment = use_case.execute("Nice", 1, 1)
        
        assert comment.id == 1
        mock_comment_repo.create.assert_called_once()


class TestAPI:
    def test_create_user(self, client):
        response = client.post('/users', json={
            "username": "testuser",
            "email": "test@example.com"
        })
        assert response.status_code == 201
        data = response.json
        assert data['username'] == "testuser"
        assert data['email'] == "test@example.com"
        assert 'id' in data

    def test_create_post(self, client):
        user_resp = client.post('/users', json={
            "username": "author",
            "email": "author@example.com"
        })
        user_id = user_resp.json['id']
        
        response = client.post('/posts', json={
            "title": "Test Post",
            "content": "This is a test post",
            "author_id": user_id
        })
        assert response.status_code == 201
        data = response.json
        assert data['title'] == "Test Post"
        assert data['author_id'] == user_id
        assert 'id' in data

    def test_get_post(self, client):
        user_resp = client.post('/users', json={
            "username": "author",
            "email": "author@example.com"
        })
        user_id = user_resp.json['id']
        
        post_resp = client.post('/posts', json={
            "title": "Get Post Test",
            "content": "Content for get test",
            "author_id": user_id
        })
        post_id = post_resp.json['id']
        
        response = client.get(f'/posts/{post_id}')
        assert response.status_code == 200
        data = response.json
        assert data['id'] == post_id
        assert data['title'] == "Get Post Test"

    def test_get_nonexistent_post(self, client):
        response = client.get('/posts/999')
        assert response.status_code == 404
        assert response.json == {'error': 'Post not found'}

    def test_create_comment(self, client):
        user_resp = client.post('/users', json={
            "username": "commenter",
            "email": "commenter@example.com"
        })
        user_id = user_resp.json['id']
        
        post_resp = client.post('/posts', json={
            "title": "Comment Test",
            "content": "Post for comments",
            "author_id": user_id
        })
        post_id = post_resp.json['id']
        
        response = client.post('/comments', json={
            "content": "Nice post!",
            "post_id": post_id,
            "author_id": user_id
        })
        assert response.status_code == 201
        data = response.json
        assert data['content'] == "Nice post!"
        assert data['post_id'] == post_id
        assert data['author_id'] == user_id

    def test_create_post_with_invalid_user(self, client):
        response = client.post('/posts', json={
            "title": "Invalid User",
            "content": "Should fail",
            "author_id": 999
        })
        assert response.status_code == 400
        assert response.json == {'error': 'Author with ID 999 does not exist'}


class TestDatabase:
    def test_user_model(self, app):
        with app.app_context():
            user = UserModel(username="dbuser", email="dbuser@example.com")
            db.session.add(user)
            db.session.commit()
            
            fetched = UserModel.query.first()
            assert fetched.username == "dbuser"
            assert fetched.email == "dbuser@example.com"

    def test_post_model(self, app):
        with app.app_context():
            user = UserModel(username="author", email="author@example.com")
            db.session.add(user)
            db.session.commit()
            
            post = PostModel(title="DB Test", content="Database content", author_id=user.id)
            db.session.add(post)
            db.session.commit()
            
            fetched = PostModel.query.first()
            assert fetched.title == "DB Test"
            assert fetched.author_id == user.id

    def test_comment_model(self, app):
        with app.app_context():
            user = UserModel(username="commenter", email="commenter@example.com")
            db.session.add(user)
            db.session.commit()
            
            post = PostModel(title="Comment Test", content="Post content", author_id=user.id)
            db.session.add(post)
            db.session.commit()
            
            comment = CommentModel(content="Test comment", post_id=post.id, author_id=user.id)
            db.session.add(comment)
            db.session.commit()
            
            fetched = CommentModel.query.first()
            assert fetched.content == "Test comment"
            assert fetched.post_id == post.id
            assert fetched.author_id == user.id