import os, json
from procstream import DataSourceService
import logging as logger

new_config = {"FILE_NAME": os.environ.get("FILE_NAME", "")}


class FileReader():

    def __init__(self, datasource_service_obj, file_name):
        self.datasource_service_obj = datasource_service_obj
        self.file_name = file_name

    def file_data_producer(self):
        logger.info("Reading File and producing to Kafka...")
        with open(self.file_name, 'r') as reader:
            for line in reader.readlines():
                self.datasource_service_obj.produce_to_topic(line)


# def main():
#     datasource_service_obj = DataSourceService(new_config)
#
#     file_reader = FileReader(datasource_service_obj, new_config.get("FILE_NAME"))
#
#     file_reader.file_data_producer()
