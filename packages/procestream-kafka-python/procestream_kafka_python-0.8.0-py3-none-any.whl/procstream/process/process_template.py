from abc import ABC, abstractmethod
from kafka import KafkaProducer
from kafka import KafkaConsumer
import logging as logger
import json
import os

logger.basicConfig(format='%(asctime)s|[%(levelname)s]|File:%(filename)s|'
                          'Function:%(funcName)s|Line:%(lineno)s|%(message)s')

default_config = {"KAFKA_SOURCE_BOOTSTRAP_SERVERS": os.environ.get("KAFKA_SOURCE_BOOTSTRAP_SERVERS",
                                                                   ''),
                  "KAFKA_SOURCE_TOPIC": os.environ.get('KAFKA_SOURCE_TOPIC', ''),
                  "KAFKA_TARGET_BOOTSTRAP_SERVERS": os.environ.get("KAFKA_TARGET_BOOTSTRAP_SERVERS",
                                                                   ''),
                  "KAFKA_TARGET_TOPIC": os.environ.get('KAFKA_TARGET_TOPIC', ''),
                  "MODULE_NAME": os.environ.get('MODULE_NAME', ''),
                  "CONSUMER_GROUP": os.environ.get("CONSUMER_GROUP", '')}

""" Base Class for pipeline module """


class StreamProcessMicroService(ABC):

    @staticmethod
    def forgiving_json_deserializer(v):
        if v is None:
            return
        try:
            return json.loads(v.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            logger.error('Unable to decode: %s', v)
            return None

    def __init__(self, new_config):
        self.config = {**default_config, **new_config}
        self.verify_env()
        logger.info("Connecting to Kafka Consumer bootstrap server")
        self.consumer_client = KafkaConsumer(self.config.get("KAFKA_SOURCE_TOPIC"),
                                             group_id=self.config.get("CONSUMER_GROUP"),
                                             bootstrap_servers=self.config.get("KAFKA_SOURCE_BOOTSTRAP_SERVERS").split(
                                                 ","),
                                             value_deserializer=lambda v: self.forgiving_json_deserializer(v))
        logger.info("Connecting to Kafka Producer bootstrap server")
        self.producer_client = KafkaProducer(
            bootstrap_servers=self.config.get("KAFKA_TARGET_BOOTSTRAP_SERVERS").split(","),
            value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.target_topic = self.config.get("KAFKA_TARGET_TOPIC")

    def verify_env(self):
        verification_failed = False
        for key, value in self.config.items():
            if not str.strip(value):
                verification_failed = True
                logger.error(f"Environment variable '{key}' not set.")
        if verification_failed:
            quit(1)

    def get_producer_client(self):
        return self.producer_client

    def get_consumer_client(self):
        return self.consumer_client

    @abstractmethod
    def process_message(self, message):
        """ Abstract Method. Override this to process the message """
        raise NotImplementedError('Implement me in subclass')

    def kafka_pipeline_service(self):
        """ Skeleton of operations to perform. DON'T override """
        print("Starting consumer")
        for message in self.consumer_client:
            processed_message = self.process_message(message)
            if processed_message:
                self.producer_client.send(self.target_topic, processed_message)

    def start_service(self):
        self.kafka_pipeline_service()
