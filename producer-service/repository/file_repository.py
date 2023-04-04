import uuid
from os import makedirs

from fastapi import Depends

from config.config import Config


class FileRepository():
    def __init__(self,
                 config: Config = Depends()) -> None:
        self.local_images_dir = config.LOCAL_IMAGES_DIR

    async def get_file_by_name(self, filename: str) -> bytes:
        pass

    async def save_file(self, content_type: str, file_binary: bytes) -> str:
        try:
            makedirs(name=self.local_images_dir,
                     mode=0o777,
                     exist_ok=True)
        except Exception as e:
            raise Exception(e)

        filename = f'{uuid.uuid4()}.{content_type.split("/")[-1]}'
        try:
            with open(f'{self.local_images_dir}/{filename}', 'wb') as file:
                file.write(file_binary)
        except Exception as e:
            raise Exception(e)

        return filename
