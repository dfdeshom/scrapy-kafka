from scrapy_kafka.connection import from_settings
from scrapy.utils.serialize import ScrapyJSONEncoder

class KafkaPipeline(object):
    """Publishes a serialized item into a Kafka toppic"""
    def __init__(self, producer, topic):
        self.producer = producer
        self.topic = topic
        self.encoder = ScrapyJSONEncoder()
        
    def process_item(self, item, spider):
        # put spider name in item
        item = dict(item)
        item['spider'] = spider.name
        msg = self.encoder.encode(item)
        self.producer.send_messages(self.topic,msg)
    
    @classmethod
    def from_settings(cls, settings):
        conn, topic = from_settings(settings)
        return cls(conn,topic)
    
