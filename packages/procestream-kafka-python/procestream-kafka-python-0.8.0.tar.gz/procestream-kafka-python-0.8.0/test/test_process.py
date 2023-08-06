from unittest import TestCase
from procstream import StreamProcessMicroService


class StreamProcessTestImpl(StreamProcessMicroService):
    def process_message(self, message):
        print(message)
        return message


class Test(TestCase):

    def setUp(self) -> None:
        config = {"KAFKA_TARGET_BOOTSTRAP_SERVERS": "localhost",
                  "KAFKA_SOURCE_BOOTSTRAP_SERVERS": "localhost",
                  "KAFKA_SOURCE_TOPIC": "topic1",
                  "KAFKA_TARGET_TOPIC": "topic2",
                  "CONSUMER_GROUP": "cg01",
                  "MODULE_NAME": 'test_module'}

        self.k_service = StreamProcessTestImpl(config)

    def test_kafka_producer_connection(self):
        self.assertTrue(self.k_service.get_producer_client().bootstrap_connected())

    def test_kafka_consumer_connection(self):
        self.assertTrue(self.k_service.get_consumer_client().bootstrap_connected())
