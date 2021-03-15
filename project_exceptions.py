
class NoDatabaseError( Exception):
        def __init__(self, message = "Can't find database"):
            self.message = message
            super().__init__(self.message)