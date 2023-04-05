import re
from io import BytesIO

from fastapi import Depends

from broker.rabbitmq import RabbitMQ, get_rabbitmq_instance
from repository.image_repository import ImageRepository
from repository.file_repository import FileRepository
from models.image_model import ImageModel


class ImageService():
    def __init__(self,
                 broker: RabbitMQ = Depends(get_rabbitmq_instance),
                 file_repository: FileRepository = Depends(),
                 image_repository: ImageRepository = Depends()) -> None:
        self.broker = broker
        self.file_repository = file_repository
        self.image_repository = image_repository


    async def get_image_by_id(self, id: int) -> tuple:
        try:
            image: ImageModel = await self.image_repository.get_image_by_id(id=id)
        except Exception as e:
            raise Exception(e)

        try:
            file_binary: bytes = await self.file_repository.get_file_by_name(image.filename)
        except Exception as e:
            raise Exception(e)

        result = BytesIO(file_binary)
        result.seek(0)

        return result, str(image.filename).split('.')[-1]


    async def upload_image(self,
                           content_type: str,
                           file_binary: bytes) -> int:
        try:
            filename: str = await self.file_repository.save_file(content_type=content_type,
                                                                 file_binary=file_binary)
            saved_file: ImageModel = await self.image_repository.save_image(filename=filename)
        except Exception as e:
            raise Exception(e)

        return saved_file.id


    async def process_image_by_id(self,
                                  id: int,
                                  action: str):

        message = f'id={id},action={action}'
        await self.broker.publish(message=message)

