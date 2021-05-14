class ValidationError(RuntimeError):
    """Exception caused by validation failure"""

    def __init__(self, description: str):
        self.description = description

    @property
    def message(self):
        return self.description
