import pika
from pika import spec

from config.config import Config, config


class RabbitMQ:
    def __init__(self,
                 config: Config = config) -> None:
        self.credentials = pika.PlainCredentials(username=config.MESSAGE_BROKER_USER,
                                            password=config.MESSAGE_BROKER_PASSWORD)
        self.connection_parameters = pika.ConnectionParameters(host=config.MESSAGE_BROKER_HOST,
                                                               port=config.MESSAGE_BROKER_PORT,
                                                               credentials=self.credentials)
        self.connection = None

    def connect(self) -> None:
        self.connection = pika.BlockingConnection(self.connection_parameters)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='images_exchange',
                                      exchange_type='direct',
                                      durable=True)
        self.channel.queue_declare(queue='images_for_process_queue',
                                   durable=True)
        self.channel.queue_bind(queue='images_for_process_queue',
                                exchange='images_exchange',
                                routing_key='image_process')


    async def publish(self, message: str) -> None:
        self.channel.basic_publish(exchange='images_exchange',
                                   routing_key='image_process',
                                   body=message,
                                   properties=pika.BasicProperties(delivery_mode=spec.PERSISTENT_DELIVERY_MODE))


rabbitmq_instance = RabbitMQ()


def get_rabbitmq_instance() -> RabbitMQ:
    while True:
        if rabbitmq_instance.connection == None or rabbitmq_instance.connection.is_closed:
            rabbitmq_instance.connect()
        else:
            return rabbitmq_instance
