from sqlalchemy.orm import Session

from models.image_model import ImageModel
from database.database import get_session


class ImageRepository():
    def __init__(self) -> None:
        self.db_session: Session = get_session()

    def get_image_by_id(self, id: int) -> ImageModel:
        image: ImageModel = self.db_session.get(ImageModel, id)
        return image

    def save_image(self, filename: str) -> ImageModel:
        image: ImageModel = ImageModel(
            filename=filename,
        )

        self.db_session.add(image)
        self.db_session.commit()
        self.db_session.refresh(image)

        return image
