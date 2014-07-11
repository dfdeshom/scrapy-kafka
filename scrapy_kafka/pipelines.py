from scrapy_kafka.connection import from_settings
from scrapy.utils.serialize import ScrapyJSONEncoder

class KafkaPipeline(object):

    def __init__(self, cluster, topic):
        self.cluster = cluster
        self.encoder = ScrapyJSONEncoder()
        self.topic = topic
        
    def process_item(self, item, spider):
        # put spider name in item
        item['spider'] = spider.name
        msg = self.encoder.encode(item)
        self.cluster.topics[self.topic].publish(msg)
    
    @classmethod
    def from_settings(cls, settings):
        return cls(from_settings(settings),settings.get('KAFKA_TOPIC'))
    
