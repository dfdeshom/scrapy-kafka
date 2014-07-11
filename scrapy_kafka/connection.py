#from kazoo.client import KazooClient
#from samsa.cluster import Cluster
from kafka.client import KafkaClient
from kafka.producer import SimpleProducer

# defaulf values
KAFKA_HOSTS = ['localhost:9092']
KAFKA_TOPIC = 'scrapy_kafka_item'

def from_settings(settings):
    k_hosts = settings.get('KAFKA_HOSTS',KAFKA_HOSTS)
    topic = settings.get('KAFKA_TOPIC',KAFKA_TOPIC)
    kafka = KafkaClient(k_hosts)
    producer = SimpleProducer(kafka)
    return producer,topic
