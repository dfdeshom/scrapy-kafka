from scrapy import signals
from scrapy import log
from scrapy.exceptions import DontCloseSpider
from scrapy.spider import Spider

from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer

class KafkaSpiderMixin(object):
    """Mixin class to implement reading urls from a kafka queue."""
    topic = None

    def setup_kafka(self,settings):
        """Setup redis connection and idle signal.

        This should be called after the spider has set its crawler object.
        """
        if not self.topic:
            self.topic = '%s-starturls' % self.name

        hosts = settings.get('SCRAPY_KAFKA_HOSTS',['localhost:9092'])
        consumer_group = settings.get('SCRAPY_KAFKA_SPIDER_CONSUMER_GROUP','scrapy-kafka')
        _kafka = KafkaClient(hosts)
        # wait atr most 1sec for more messages. Otherwise contiunue
        self.consumer = SimpleConsumer(_kafka,consumer_group,self.topic,
                                       auto_commit=False, iter_timeout=1.0)
        # idle signal is called when the spider has no requests left,
        # that's when we will schedule new requests from kafka topic
        self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        self.crawler.signals.connect(self.item_scraped, signal=signals.item_scraped)
        self.log("Reading URLs from kafka topic '%s'" % self.topic)

    # def start_requests(self):
    #     for om in self.consumer:
    #         url = om.message.value
    #         if url:
    #             print 'url ', url
    #             yield self.make_requests_from_url(url)
            
        
    def next_request(self):
        """Returns a request to be scheduled or none."""
        #message = self.consumer.get_messages(1)[0]
        message = self.consumer.get_message(True)
        print 'msg ', message
        if not message:
            return None
        
        url = message.message.value
        if not url:
            return None
        print 'url is ', url
        return self.make_requests_from_url(url)
        
        # for om in self.consumer:
        #     url = om.message.value
        #     print 'url ', url
        #     if url:
        #         return self.make_requests_from_url(url)
                
    def schedule_next_request(self):
        """Schedules a request if available"""
        req = self.next_request()
        if req:
            self.crawler.engine.crawl(req, spider=self)

    def spider_idle(self):
        """Schedules a request if available, otherwise waits."""
        self.schedule_next_request()
        raise DontCloseSpider

    def item_scraped(self, *args, **kwargs):
        """Avoids waiting for the spider to  idle before scheduling the next request"""
        self.schedule_next_request()


class KafkaSpider(KafkaSpiderMixin, Spider):
    """Spider that reads urls from redis queue when idle."""

    def set_crawler(self, crawler):
        super(KafkaSpider, self).set_crawler(crawler)
        self.setup_kafka(crawler.settings)
