class InvalidCategoryException(Exception):
    def __init__(self, message="Invalid Category"):
        self.message = message

