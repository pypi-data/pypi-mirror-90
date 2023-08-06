from abc import ABC
from kafka import KafkaProducer
import logging as logger
import json
import os

default_config = {"KAFKA_TARGET_BOOTSTRAP_SERVERS": os.environ.get("KAFKA_TARGET_BOOTSTRAP_SERVERS",
                                                                   ''),
                  "KAFKA_TARGET_TOPIC": os.environ.get("KAFKA_TARGET_TOPIC", ""),
                  "MODULE_NAME": os.environ.get("MODULE_NAME", ""),
                  "CONSUMER_GROUP": os.environ.get("CONSUMER_GROUP", "")}


class DataSourceService(ABC):
    def __init__(self, new_config):
        self.config = {**default_config, **new_config}
        self.verify_env()
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

    def produce_to_topic(self, data):
        self.producer_client.send(self.target_topic, data)

    def log_error(self, data):
        logger.error(f"In sending record: {data}")

    def restart_collector(self, new_config):
        self.__init__(self, new_config)
