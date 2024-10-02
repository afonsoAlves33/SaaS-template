from sqlalchemy.exc import IntegrityError


class ExistingDataError(IntegrityError):
    """
    A custom exception raised when a try to create already existing data on unique fields is did.
    """
    def __init__(self, description: str = None, statement=None, params=None, orig=None):
        self.description=description
        super().__init__(statement, params, orig)
