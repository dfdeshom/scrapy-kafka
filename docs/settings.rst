========
Settings
========


SCRAPY_KAFKA_HOSTS
-------------------

Default: `['localhost:9092']`

The Kafka hosts.


SCRAPY_KAFKA_ITEM_PIPELINE_TOPIC
----------------------------------

Default: `scrapy_kafka_item`

The Kafka topic to post processed items from the pipeline to.


SCRAPY_KAFKA_SPIDER_CONSUMER_GROUP
-----------------------------------

Default : `scrapy-kafka`

The Kafka consumer group a :class:`~scrapy_kafka.spiders.ListeningKafkaSpider` belongs to.



