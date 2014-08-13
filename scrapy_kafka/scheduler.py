from kafka.consumer import SimpleConsumer
from kafka.producer import SimpleProducer

from scrapy.utils.reqser import request_to_dict, request_from_dict
from scrapy.utils.misc import load_object
from scrapy.utils.job import job_dir
from scrapy import log

from queues import KafkaLIFOQueue


class KafkaScheduler(object):

    """
    A Kafka-based sheduler
    """

    def __init__(self, kafka_host, scheduler_topic, consumer_group,
                 queue, dupefilter, logunser=False):
        self.df = dupefilter
        self.logunser = logunser
        self.kafka_host = kafka_host
        self.consumer_group = consumer_group
        self.scheduler_topic = scheduler_topic
        self.queue = queue
        self.consumer = SimpleConsumer(kafka_host, consumer_group, scheduler_topic,
                                       auto_commit=True, iter_timeout=1.0)
        self.producer = SimpleProducer(kafka_host)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        dupefilter_cls = load_object(settings['DUPEFILTER_CLASS'])
        dupefilter = dupefilter_cls.from_settings(settings)
        queue = KafkaLIFOQueue  # XXX for now
        kafka_host = settings.get('SCRAPY_KAFKA_HOSTS', ['localhost:9092'])
        logunser = settings.getbool('LOG_UNSERIALIZABLE_REQUESTS')
        consumer_group = settings.get('SCRAPY_KAFKA_SPIDER_CONSUMER_GROUP', 'scrapy-kafka')
        scheduler_topic = settings.get('SCRAPY_KAFKA_SCHEDULER_TOPIC', 'scrapy-scheduler')
        return cls(kafka_host, scheduler_topic, consumer_group, queue, dupefilter, logunser)

    def has_pending_requests(self):
        return len(self) > 0

    def open(self, spider):
        self.spider = spider
        return self.df.open()

    def close(self, reason):
        return self.df.close(reason)

    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):
            self.df.log(request, self.spider)
            return

        self.queue.push(request)

    def next_request(self):
        request = self.queue.pop()
        return request

    def __len__(self):
        return len(self.queue)
