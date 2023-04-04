from typing import Callable

import pika
from pika.spec import Basic
from retry import retry

from config.config import Config, config


class RabbitMQClient:
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
        self.channel.basic_qos(prefetch_count=1)
        self.channel.exchange_declare(exchange='images_exchange',
                                      exchange_type='direct',
                                      durable=True)
        self.channel.queue_declare(queue='images_for_process_queue',
                                   durable=True)
        self.channel.queue_bind(queue='images_for_process_queue',
                                exchange='images_exchange',
                                routing_key='image_process')


    @retry(pika.exceptions.AMQPConnectionError, delay=1, backoff=2)
    def consume(self, callback_func: Callable) -> None:
        if self.connection == None or self.connection.is_closed:
            self.connect()

        try:
            self.channel.basic_consume(queue='images_for_process_queue',
                                       on_message_callback=callback_func,
                                       auto_ack=False)
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.close()
            self.connection.close()
        except Exception as e:
            print(e)
