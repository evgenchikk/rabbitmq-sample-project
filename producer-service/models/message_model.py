class ImageProcessRequestModel():
    def __init__(self, filename: str, action: str) -> None:
        self.filename = filename
        self.action = action
