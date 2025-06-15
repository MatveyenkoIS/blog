from flask import Blueprint, request, jsonify, current_app
from application.use_cases import (
    CreateUserUseCase, 
    CreatePostUseCase, 
    CreateCommentUseCase, 
    GetPostUseCase
)
from infrastructure.repositories import (
    SQLUserRepository, 
    SQLPostRepository, 
    SQLCommentRepository
)

bp = Blueprint('controllers', __name__)

user_repo = SQLUserRepository()
post_repo = SQLPostRepository()
comment_repo = SQLCommentRepository()

create_user_uc = CreateUserUseCase(user_repo)
create_post_uc = CreatePostUseCase(post_repo, user_repo)
create_comment_uc = CreateCommentUseCase(comment_repo, post_repo, user_repo)
get_post_uc = GetPostUseCase(post_repo)


@bp.route('/')
def index():
    """
    API Information
    ---
    tags:
      - general
    responses:
      200:
        description: API information
        schema:
          type: object
          properties:
            message:
              type: string
            endpoints:
              type: object
    """
    return jsonify({
        'message': 'Welcome to Blog API',
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
    Create a new user
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
        description: User created
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
        current_app.logger.error(f"Error creating post: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """
    Get a post by ID
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
        description: Post found
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
        description: Post not found
    """
    post = get_post_uc.execute(post_id)
    if post:
        return jsonify({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author_id': post.author_id
        })
    return jsonify({'error': 'Post not found'}), 404


@bp.route('/comments', methods=['POST'])
def create_comment():
    """
    Create a new comment
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
              example: Nice post!
            post_id:
              type: integer
              example: 1
            author_id:
              type: integer
              example: 1
    responses:
      201:
        description: Comment created
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