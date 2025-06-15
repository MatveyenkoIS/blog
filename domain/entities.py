class User:
    def __init__(self, id: int, username: str, email: str):
        self.id = id
        self.username = username
        self.email = email

class Post:
    def __init__(self, id: int, title: str, content: str, author_id: int):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id

class Comment:
    def __init__(self, id: int, content: str, post_id: int, author_id: int):
        self.id = id
        self.content = content
        self.post_id = post_id
        self.author_id = author_id