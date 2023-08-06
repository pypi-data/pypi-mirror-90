class NoteNotFoundError(Exception):

    def __init__(self, message="The Specified note couldn't be found"):
        super().__init__(message)

class WallNotFoundError(Exception):
    
    def __init__(self, message="The Specified wall couldn't be found"):
        super().__init__(message)

class NoParentTrack(Exception):

    def __init__(self, message="The Specified wall couldn't be found"):
        super().__init__(message)