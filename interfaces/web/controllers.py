from flask import Blueprint, request, jsonify, current_app
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
from infrastructure.repositories import (
    SQLUserRepository, 
    SQLPostRepository, 
    SQLCommentRepository
)

bp = Blueprint('controllers', __name__)

# Инициализация репозиториев
user_repo = SQLUserRepository()
post_repo = SQLPostRepository()
comment_repo = SQLCommentRepository()

# Инициализация сценариев использования
create_user_uc = CreateUserUseCase(user_repo)
create_post_uc = CreatePostUseCase(post_repo, user_repo)
create_comment_uc = CreateCommentUseCase(comment_repo, post_repo, user_repo)
get_post_uc = GetPostUseCase(post_repo)
get_all_users_uc = GetAllUsersUseCase(user_repo)
get_user_by_id_uc = GetUserByIdUseCase(user_repo)
delete_user_uc = DeleteUserUseCase(user_repo)
get_all_posts_uc = GetAllPostsUseCase(post_repo)
delete_post_uc = DeletePostUseCase(post_repo)
get_all_comments_uc = GetAllCommentsUseCase(comment_repo)
get_comment_by_id_uc = GetCommentByIdUseCase(comment_repo)
delete_comment_uc = DeleteCommentUseCase(comment_repo)


@bp.route('/')
def index():
    """
    Информация о API.
    ---
    tags:
      - general
    responses:
      200:
        description: Информация о API
        schema:
          type: object
          properties:
            message:
              type: string
            endpoints:
              type: object
    """
    return jsonify({
        'message': 'Добро пожаловать в Blog API',
        'endpoints': {
            'create_user': 'POST /users',
            'create_post': 'POST /posts',
            'get_post': 'GET /posts/<int:post_id>',
            'create_comment': 'POST /comments'
        }
    })


@bp.route('/users', methods=['POST'])
def create_user():
    """
    Создать нового пользователя.
    ---
    tags:
      - users
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - username
            - email
          properties:
            username:
              type: string
              example: testuser
            email:
              type: string
              example: test@example.com
    responses:
      201:
        description: Пользователь создан
        schema:
          type: object
          properties:
            id:
              type: integer
            username:
              type: string
            email:
              type: string
    """
    data = request.json
    user = create_user_uc.execute(data['username'], data['email'])
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    }), 201


@bp.route('/posts', methods=['POST'])
def create_post():
    """
    Создать новую публикацию.
    ---
    tags:
      - posts
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - title
            - content
            - author_id
          properties:
            title:
              type: string
              example: Первая публикация
            content:
              type: string
              example: Привет мир!
            author_id:
              type: integer
              example: 1
    responses:
      201:
        description: Публикация создана
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            content:
              type: string
            author_id:
              type: integer
      400:
        description: Неверные входные данные
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Внутренняя ошибка сервера
    """
    data = request.json
    try:
        post = create_post_uc.execute(
            data['title'], 
            data['content'], 
            data['author_id']
        )
        return jsonify({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author_id': post.author_id
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Ошибка при создании публикации: {str(e)}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500


@bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """
    Получить публикацию по ID.
    ---
    tags:
      - posts
    parameters:
      - name: post_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Публикация найдена
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            content:
              type: string
            author_id:
              type: integer
      404:
        description: Публикация не найдена
    """
    post = get_post_uc.execute(post_id)
    if post:
        return jsonify({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author_id': post.author_id
        })
    return jsonify({'error': 'Публикация не найдена'}), 404


@bp.route('/comments', methods=['POST'])
def create_comment():
    """
    Создать новый комментарий.
    ---
    tags:
      - comments
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - content
            - post_id
            - author_id
          properties:
            content:
              type: string
              example: Отличная публикация!
            post_id:
              type: integer
              example: 1
            author_id:
              type: integer
              example: 1
    responses:
      201:
        description: Комментарий создан
        schema:
          type: object
          properties:
            id:
              type: integer
            content:
              type: string
            post_id:
              type: integer
            author_id:
              type: integer
    """
    data = request.json
    comment = create_comment_uc.execute(
        data['content'], 
        data['post_id'], 
        data['author_id']
    )
    return jsonify({
        'id': comment.id,
        'content': comment.content,
        'post_id': comment.post_id,
        'author_id': comment.author_id
    }), 201


@bp.route('/users', methods=['GET'])
def get_all_users():
    """
    Получить всех пользователей.
    ---
    tags:
      - users
    responses:
      200:
        description: Список пользователей
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              username:
                type: string
              email:
                type: string
    """
    users = get_all_users_uc.execute()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email
    } for u in users])


@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Получить пользователя по ID.
    ---
    tags:
      - users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Пользователь найден
        schema:
          type: object
          properties:
            id:
              type: integer
            username:
              type: string
            email:
              type: string
      404:
        description: Пользователь не найден
    """
    user = get_user_by_id_uc.execute(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })
    return jsonify({'error': 'Пользователь не найден'}), 404


@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Удалить пользователя по ID.
    ---
    tags:
      - users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Пользователь удален
      404:
        description: Пользователь не найден
    """
    user = get_user_by_id_uc.execute(user_id)
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404
    
    delete_user_uc.execute(user_id)
    return '', 204


@bp.route('/posts', methods=['GET'])
def get_all_posts():
    """
    Получить все публикации.
    ---
    tags:
      - posts
    responses:
      200:
        description: Список публикаций
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              content:
                type: string
              author_id:
                type: integer
    """
    posts = get_all_posts_uc.execute()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'content': p.content,
        'author_id': p.author_id
    } for p in posts])


@bp.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Удалить публикацию по ID.
    ---
    tags:
      - posts
    parameters:
      - name: post_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Публикация удалена
      404:
        description: Публикация не найдена
    """
    post = get_post_uc.execute(post_id)
    if not post:
        return jsonify({'error': 'Публикация не найдена'}), 404
    
    delete_post_uc.execute(post_id)
    return '', 204


@bp.route('/comments', methods=['GET'])
def get_all_comments():
    """
    Получить все комментарии.
    ---
    tags:
      - comments
    responses:
      200:
        description: Список комментариев
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              content:
                type: string
              post_id:
                type: integer
              author_id:
                type: integer
    """
    comments = get_all_comments_uc.execute()
    return jsonify([{
        'id': c.id,
        'content': c.content,
        'post_id': c.post_id,
        'author_id': c.author_id
    } for c in comments])


@bp.route('/comments/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    """
    Получить комментарий по ID.
    ---
    tags:
      - comments
    parameters:
      - name: comment_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Комментарий найден
        schema:
          type: object
          properties:
            id:
              type: integer
            content:
              type: string
            post_id:
              type: integer
            author_id:
              type: integer
      404:
        description: Комментарий не найден
    """
    comment = get_comment_by_id_uc.execute(comment_id)
    if comment:
        return jsonify({
            'id': comment.id,
            'content': comment.content,
            'post_id': comment.post_id,
            'author_id': comment.author_id
        })
    return jsonify({'error': 'Комментарий не найден'}), 404


@bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """
    Удалить комментарий по ID.
    ---
    tags:
      - comments
    parameters:
      - name: comment_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Комментарий удален
      404:
        description: Комментарий не найден
    """
    comment = get_comment_by_id_uc.execute(comment_id)
    if not comment:
        return jsonify({'error': 'Комментарий не найден'}), 404
    
    delete_comment_uc.execute(comment_id)
    return '', 204