import traceback

from procstream.sink.data_sink import DataSinkService
from elasticsearch import Elasticsearch
import os
import logging as logger

config = {"ES_MAXSIZE": os.environ.get("ES_MAXSIZE", "25"),
          "ES_SNIFFER_TIMEOUT": os.environ.get("ES_SNIFFER_TIMEOUT", "60"),
          "MODULE_NAME": os.environ.get("MODULE_NAME", ""),
          "CONSUMER_GROUP": os.environ.get("CONSUMER_GROUP", ""),
          "ES_HOST": os.environ.get('ES_HOST', ''),
          "ES_INDEX": os.environ.get('ES_INDEX', ''),
          "ES_DOCTYPE": os.environ.get('ES_DOCTYPE', '_doc')
          }


class ElasticSearchDataSinkService(DataSinkService):

    def __init__(self, new_config={}):
        new_config = {**config, **new_config}
        super().__init__(new_config)
        logger.info("Initializing ES Injector Module")
        self.es_host = new_config.get("ES_HOST")
        self.es_maxsize = int(new_config.get("ES_MAXSIZE"))
        self.es_sniffer_timeout = int(new_config.get("ES_SNIFFER_TIMEOUT"))
        self.es_index = new_config.get("ES_INDEX")
        self.es_doctype = new_config.get("ES_DOCTYPE")
        self.es = Elasticsearch([self.es_host], maxsize=self.es_maxsize, sniff_on_start=True,
                                sniff_on_connection_fail=True,
                                sniffer_timeout=self.es_sniffer_timeout, retry_on_timeout=True)

    def insert_record(self, message):
        try:
            res = self.es.index(index=self.es_index, doc_type=self.es_doctype, body=message.value)
            print(res['result'])
        except:
            logger.error(f"Cannot ingest record:{message.value}")
            traceback.print_exc()
