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

user_repo = SQLUserRepository()
post_repo = SQLPostRepository()
comment_repo = SQLCommentRepository()

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
    """
    Create a new post
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
              example: First Post
            content:
              type: string
              example: Hello World!
            author_id:
              type: integer
              example: 1
    responses:
      201:
        description: Post created
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
        description: Invalid input
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Internal server error
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

@bp.route('/users', methods=['GET'])
def get_all_users():
    """
    Get all users
    ---
    tags:
      - users
    responses:
      200:
        description: List of users
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
    Get a user by ID
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
        description: User found
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
        description: User not found
    """
    user = get_user_by_id_uc.execute(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })
    return jsonify({'error': 'User not found'}), 404

@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user by ID
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
        description: User deleted
      404:
        description: User not found
    """
    user = get_user_by_id_uc.execute(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    delete_user_uc.execute(user_id)
    return '', 204

@bp.route('/posts', methods=['GET'])
def get_all_posts():
    """
    Get all posts
    ---
    tags:
      - posts
    responses:
      200:
        description: List of posts
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
    Delete a post by ID
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
        description: Post deleted
      404:
        description: Post not found
    """
    post = get_post_uc.execute(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    delete_post_uc.execute(post_id)
    return '', 204

@bp.route('/comments', methods=['GET'])
def get_all_comments():
    """
    Get all comments
    ---
    tags:
      - comments
    responses:
      200:
        description: List of comments
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
    Get a comment by ID
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
        description: Comment found
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
        description: Comment not found
    """
    comment = get_comment_by_id_uc.execute(comment_id)
    if comment:
        return jsonify({
            'id': comment.id,
            'content': comment.content,
            'post_id': comment.post_id,
            'author_id': comment.author_id
        })
    return jsonify({'error': 'Comment not found'}), 404

@bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """
    Delete a comment by ID
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
        description: Comment deleted
      404:
        description: Comment not found
    """
    comment = get_comment_by_id_uc.execute(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    delete_comment_uc.execute(comment_id)
    return '', 204