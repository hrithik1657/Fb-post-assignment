class InvalidUserException(Exception):
    def __init__(self):
        super().__init__("User id not found")


class InvalidPostContent(Exception):
    def __init__(self):
        super().__init__("post_content is empty")


class InvalidPostException(Exception):
    def __init__(self):
        super().__init__("post id not found")


class InvalidCommentException(Exception):
    def __init__(self):
        super().__init__("comment id not found")


class InvalidCommentContent(Exception):
    def __init__(self):
        super().__init__("comment_content nis empty")


class InvalidReactionContent(Exception):
    def __init__(self):
        super().__init__("Reaction does not exist")
