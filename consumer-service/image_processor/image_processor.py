import re

from pika.channel import Channel
from pika.spec import Basic
from PIL import Image

from models.image_model import ImageModel
from repository.image_repository import ImageRepository
from config.config import config


def resize(image: Image.Image, w: int, h: int) -> Image.Image:
    return image.resize((w,h))


def grayscale(image: Image.Image) -> Image.Image:
    return image.convert('L')


def save(image: Image.Image, filename: str) -> None:
    image.save(f'{config.LOCAL_IMAGES_DIR}/{filename}')


def image_processor(channel: Channel, method: Basic.Deliver, properties, body: bytes):
    body = body.decode('utf-8')

    match = re.match(r'^(id=\d+),action=(((resize)\s+(\d+,\d+))|(grayscale)\s*)$', body)
    if match == None:
        print('Wrong message format:', body)
        channel.basic_reject(requeue=False)
        return

    id = match[1].split('=')[1]

    image_repository = ImageRepository()
    try:
        image: ImageModel = image_repository.get_image_by_id(id=id)
    except Exception as e:
        print(f'{str(e)}. Message will be requeued')
        channel.basic_reject(requeue=False)
        return

    filename = image.filename

    try:
        image: Image.Image = Image.open(f'{config.LOCAL_IMAGES_DIR}/{filename}')
    except FileNotFoundError:
        print(e)
        channel.basic_reject(requeue=False)
        return
    except Exception as e:
        print(e)
        channel.basic_nack(requeue=True)
        return


    if match[2] == 'grayscale':
        image = grayscale(image)
    elif match[4] == 'resize':
        h, w = match[5].split(',')
        image = resize(image, int(w), int(h))

    try:
        save(image, filename)
    except Exception as e:
        print('Failed on saving modified file, message will be requeued. Error: ', e)
        channel.basic_nack(requeue=True)

    channel.basic_ack(delivery_tag=method.delivery_tag)
    return
