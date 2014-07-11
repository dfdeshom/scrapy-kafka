from kazoo.client import KazooClient
from samsa.cluster import Cluster

# defaulf values
ZOOKEEPER_HOSTS = ['localhost:2181',]
KAFKA_TOPIC = 'scrapy_kafka_pipeline'
KAFKA_CONSUMER_GROUP = 'scrapy_kafka'

def from_settings(settings):
    zk_hosts = settings.get('ZOOKEEPER_HOSTS',ZOOKEEPER_HOSTS)
    zk_hosts = ",".join(zk_hosts)    

    topic = settings.get('KAFKA_TOPIC',KAFKA_TOPIC)
    consumer_group = settings.get('KAFKA_CONSUMER_GROUP',KAFKA_CONSUMER_GROUP)
    
    zk = KazooClient(zk_hosts)
    zk.start()
    cluster = Cluster(zk)
    return cluster

