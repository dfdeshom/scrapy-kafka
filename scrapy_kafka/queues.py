# -*- coding: utf-8 -*-

from kafka.consumer import SimpleConsumer
from kafka.producer import SimpleProducer
from scrapy.utils.project import get_project_settings
from scrapy.utils.reqser import request_to_dict, request_from_dict
import cPickle as pickle


class KafkaLIFOQueue(object):

    """
    Per-spider FIFO queue
    """

    def __init__(self, server, spider):
        self.server = server
        self.spider = spider
        settings = get_project_settings()
        consumer_group = settings.get('SCRAPY_KAFKA_SPIDER_CONSUMER_GROUP', 'scrapy-kafka')
        self.topic = settings.get('SCRAPY_KAFKA_SCHEDULER_TOPIC', 'scrapy-scheduler')
        self.consumer = SimpleConsumer(server, consumer_group, self.topic,
                                       auto_commit=True, iter_timeout=1.0)
        self.producer = SimpleProducer(server)

    def push(self, request):
        msg = self._encode_request(request)
        self.producer.send_messages(self.topic, msg)

    def pop(self):
        msg = self.consumer.get_message(True)
        return self._decode_request(msg)

    def len(self):
        return self.consumer.pending()

    def _encode_request(self, request):
        """Encode a request object"""
        return pickle.dumps(request_to_dict(request, self.spider),
                            protocol=pickle.HIGHEST_PROTOCOL)

    def _decode_request(self, encoded_request):
        """Decode an request previously encoded"""
        return request_from_dict(pickle.loads(encoded_request), self.spider)
