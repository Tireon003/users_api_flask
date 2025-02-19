class UserNotFoundException(Exception):
    """
    Exception for user not found.
    """

    def __init__(self, user_id: int) -> None:
        super().__init__()
        self.user_id = user_id


class UserAlreadyExistsException(Exception):
    """
    Exception for user already exists.
    """

    def __init__(self, field: str, value: str) -> None:
        super().__init__()
        self.field = field
        self.value = value
