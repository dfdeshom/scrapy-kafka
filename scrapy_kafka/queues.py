# -*- coding: utf-8 -*-

from kafka.consumer import SimpleConsumer
from kafka.producer import SimpleProducer
from kafka.client import KafkaClient

from scrapy.utils.project import get_project_settings
from scrapy.utils.reqser import request_to_dict, request_from_dict
import cPickle as pickle


class KafkaLIFOQueue(object):

    """
    Per-spider FIFO queue
    """

    def __init__(self, conn):
        self.conn = conn
        settings = get_project_settings()
        consumer_group = settings.get('SCRAPY_KAFKA_SPIDER_CONSUMER_GROUP', 'scrapy-kafka')
        self.topic = settings.get('SCRAPY_KAFKA_SCHEDULER_TOPIC', 'scrapy-scheduler')
        self.consumer = SimpleConsumer(conn, consumer_group, self.topic,
                                       auto_commit=True, iter_timeout=1.0)
        self.producer = SimpleProducer(conn)

    def push(self, request):
        msg = self._encode_request(request)
        self.producer.send_messages(self.topic, msg)

    def pop(self):
        msg = self.consumer.get_message(True)
        return self._decode_request(msg)

    def __len__(self):
        n = self.consumer.pending()
        m = abs(n)
        return m

    def _encode_request(self, request):
        """Encode a request object"""
        return pickle.dumps(request_to_dict(request),
                            protocol=pickle.HIGHEST_PROTOCOL)

    def _decode_request(self, encoded_request):
        """Decode an request previously encoded"""
        if encoded_request is None:
            return
        return request_from_dict(pickle.loads(encoded_request.message.value))
