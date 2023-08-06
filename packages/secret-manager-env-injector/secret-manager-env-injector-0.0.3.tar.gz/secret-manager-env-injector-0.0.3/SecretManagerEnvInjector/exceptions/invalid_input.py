class InvalidInputException(Exception):
    def __init__(self, msg = "Invalid input params"):
        self.message = msg
        super().__init__(self.message)