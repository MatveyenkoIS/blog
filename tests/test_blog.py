import pytest
from unittest.mock import MagicMock
from domain.entities import User, Post, Comment
from application.use_cases import (
    CreateUserUseCase, 
    CreatePostUseCase, 
    CreateCommentUseCase,
    GetPostUseCase,
    GetAllUsersUseCase,
    GetUserByIdUseCase,
    DeleteUserUseCase,
    GetAllPostsUseCase,
    DeletePostUseCase,
    GetAllCommentsUseCase,
    GetCommentByIdUseCase,
    DeleteCommentUseCase
)
from infrastructure.database import db, UserModel, PostModel, CommentModel
from interfaces.web.app import create_app


@pytest.fixture
def app():
    """Фикстура для создания тестового приложения."""
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
    """Фикстура для создания тестового клиента."""
    return app.test_client()


class TestUseCases:
    """Тесты сценариев использования."""
    
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
    
    def test_get_all_users(self):
        mock_repo = MagicMock()
        mock_repo.get_all.return_value = [
            User(1, "user1", "user1@test.com"),
            User(2, "user2", "user2@test.com")
        ]
        
        use_case = GetAllUsersUseCase(mock_repo)
        users = use_case.execute()
        
        assert len(users) == 2
        assert users[0].username == "user1"
        assert users[1].username == "user2"
    
    def test_get_user_by_id(self):
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = User(1, "test", "test@example.com")
        
        use_case = GetUserByIdUseCase(mock_repo)
        user = use_case.execute(1)
        
        assert user.id == 1
        assert user.username == "test"
    
    def test_delete_user(self):
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = User(1, "test", "test@example.com")
        
        use_case = DeleteUserUseCase(mock_repo)
        use_case.execute(1)
        
        mock_repo.delete.assert_called_once_with(1)
    
    def test_get_all_posts(self):
        mock_repo = MagicMock()
        mock_repo.get_all.return_value = [
            Post(1, "Post1", "Content1", 1),
            Post(2, "Post2", "Content2", 1)
        ]
        
        use_case = GetAllPostsUseCase(mock_repo)
        posts = use_case.execute()
        
        assert len(posts) == 2
        assert posts[0].title == "Post1"
        assert posts[1].title == "Post2"
    
    def test_delete_post(self):
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = Post(1, "Test", "Content", 1)
        
        use_case = DeletePostUseCase(mock_repo)
        use_case.execute(1)
        
        mock_repo.delete.assert_called_once_with(1)
    
    def test_get_all_comments(self):
        mock_repo = MagicMock()
        mock_repo.get_all.return_value = [
            Comment(1, "Comment1", 1, 1),
            Comment(2, "Comment2", 1, 1)
        ]
        
        use_case = GetAllCommentsUseCase(mock_repo)
        comments = use_case.execute()
        
        assert len(comments) == 2
        assert comments[0].content == "Comment1"
        assert comments[1].content == "Comment2"
    
    def test_get_comment_by_id(self):
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = Comment(1, "Nice", 1, 1)
        
        use_case = GetCommentByIdUseCase(mock_repo)
        comment = use_case.execute(1)
        
        assert comment.id == 1
        assert comment.content == "Nice"
    
    def test_delete_comment(self):
        mock_repo = MagicMock()
        mock_repo.get_by_id.return_value = Comment(1, "Test", 1, 1)
        
        use_case = DeleteCommentUseCase(mock_repo)
        use_case.execute(1)
        
        mock_repo.delete.assert_called_once_with(1)


class TestAPI:
    """Тесты API эндпоинтов."""
    
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
        assert response.json == {'error': 'Публикация не найдена'}

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
        # Заменить на русское сообщение
        assert response.json == {'error': 'Автор с ID 999 не существует'}
    
    def test_get_all_users(self, client):
        client.post('/users', json={"username": "user1", "email": "user1@test.com"})
        client.post('/users', json={"username": "user2", "email": "user2@test.com"})
        
        response = client.get('/users')
        assert response.status_code == 200
        data = response.json
        assert len(data) >= 2
        usernames = [user['username'] for user in data]
        assert "user1" in usernames
        assert "user2" in usernames
    
    def test_get_user_by_id(self, client):
        user_resp = client.post('/users', json={"username": "testuser", "email": "test@example.com"})
        user_id = user_resp.json['id']
        
        response = client.get(f'/users/{user_id}')
        assert response.status_code == 200
        data = response.json
        assert data['id'] == user_id
        assert data['username'] == "testuser"
    
    def test_delete_user(self, client):
        user_resp = client.post('/users', json={"username": "todelete", "email": "delete@test.com"})
        user_id = user_resp.json['id']
        
        response = client.delete(f'/users/{user_id}')
        assert response.status_code == 204
        
        response = client.get(f'/users/{user_id}')
        assert response.status_code == 404
    
    def test_get_all_posts(self, client):
        user_resp = client.post('/users', json={"username": "author", "email": "author@test.com"})
        user_id = user_resp.json['id']
        
        client.post('/posts', json={"title": "Post1", "content": "Content1", "author_id": user_id})
        client.post('/posts', json={"title": "Post2", "content": "Content2", "author_id": user_id})
        
        response = client.get('/posts')
        assert response.status_code == 200
        data = response.json
        assert len(data) >= 2
        titles = [post['title'] for post in data]
        assert "Post1" in titles
        assert "Post2" in titles
    
    def test_delete_post(self, client):
        user_resp = client.post('/users', json={"username": "author", "email": "author@test.com"})
        user_id = user_resp.json['id']
        
        post_resp = client.post('/posts', json={"title": "To Delete", "content": "Content", "author_id": user_id})
        post_id = post_resp.json['id']
        
        response = client.delete(f'/posts/{post_id}')
        assert response.status_code == 204
        
        response = client.get(f'/posts/{post_id}')
        assert response.status_code == 404
    
    def test_get_all_comments(self, client):
        user_resp = client.post('/users', json={"username": "commenter", "email": "commenter@test.com"})
        user_id = user_resp.json['id']
        
        post_resp = client.post('/posts', json={"title": "Post", "content": "Content", "author_id": user_id})
        post_id = post_resp.json['id']
        
        client.post('/comments', json={"content": "Comment1", "post_id": post_id, "author_id": user_id})
        client.post('/comments', json={"content": "Comment2", "post_id": post_id, "author_id": user_id})
        
        response = client.get('/comments')
        assert response.status_code == 200
        data = response.json
        assert len(data) >= 2
        contents = [comment['content'] for comment in data]
        assert "Comment1" in contents
        assert "Comment2" in contents
    
    def test_get_comment_by_id(self, client):
        user_resp = client.post('/users', json={"username": "commenter", "email": "commenter@test.com"})
        user_id = user_resp.json['id']
        
        post_resp = client.post('/posts', json={"title": "Post", "content": "Content", "author_id": user_id})
        post_id = post_resp.json['id']
        
        comment_resp = client.post('/comments', json={"content": "Test comment", "post_id": post_id, "author_id": user_id})
        comment_id = comment_resp.json['id']
        
        response = client.get(f'/comments/{comment_id}')
        assert response.status_code == 200
        data = response.json
        assert data['id'] == comment_id
        assert data['content'] == "Test comment"
    
    def test_delete_comment(self, client):
        user_resp = client.post('/users', json={"username": "commenter", "email": "commenter@test.com"})
        user_id = user_resp.json['id']
        
        post_resp = client.post('/posts', json={"title": "Post", "content": "Content", "author_id": user_id})
        post_id = post_resp.json['id']
        
        comment_resp = client.post('/comments', json={"content": "To Delete", "post_id": post_id, "author_id": user_id})
        comment_id = comment_resp.json['id']
        
        response = client.delete(f'/comments/{comment_id}')
        assert response.status_code == 204
        
        response = client.get(f'/comments/{comment_id}')
        assert response.status_code == 404


class TestDatabase:
    """Тесты работы с базой данных."""
    
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
    
    def test_cascade_delete_user(self, app):
        with app.app_context():
            user = UserModel(username="cascade_user", email="cascade@example.com")
            db.session.add(user)
            db.session.commit()
            
            post = PostModel(title="Cascade Post", content="Content", author_id=user.id)
            db.session.add(post)
            db.session.commit()
            
            comment = CommentModel(content="Cascade comment", post_id=post.id, author_id=user.id)
            db.session.add(comment)
            db.session.commit()
            
            db.session.delete(user)
            db.session.commit()
            
            assert UserModel.query.get(user.id) is None
            assert PostModel.query.get(post.id) is None
            assert CommentModel.query.get(comment.id) is None
    
    def test_cascade_delete_post(self, app):
        with app.app_context():
            user = UserModel(username="author", email="author@example.com")
            db.session.add(user)
            db.session.commit()
            
            post = PostModel(title="Post", content="Content", author_id=user.id)
            db.session.add(post)
            db.session.commit()
            
            comment = CommentModel(content="Comment", post_id=post.id, author_id=user.id)
            db.session.add(comment)
            db.session.commit()
            
            db.session.delete(post)
            db.session.commit()
            
            assert PostModel.query.get(post.id) is None
            assert CommentModel.query.get(comment.id) is None
            assert UserModel.query.get(user.id) is not None