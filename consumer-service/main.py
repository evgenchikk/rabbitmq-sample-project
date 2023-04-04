from broker.rabbitmq import RabbitMQClient
from image_processor.image_processor import image_processor


consumer: RabbitMQClient = RabbitMQClient()
consumer.consume(callback_func=image_processor)
