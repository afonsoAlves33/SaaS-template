from sqlalchemy.exc import IntegrityError


class ExistingDataError(IntegrityError):
    """
    A custom exception thrown when an attempt is made to create existing data in unique fields
    """
    def __init__(self, description: str = None, statement=None, params=None, orig=None):
        self.description=description
        super().__init__(statement, params, orig)
