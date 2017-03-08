# -*- coding: utf-8 -*-

# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'example'

SPIDER_MODULES = ['example.spiders']
NEWSPIDER_MODULE = SPIDER_MODULES[0]
ITEM_PIPELINES = [
    'example.pipelines.ExamplePipeline',
    'scrapy_kafka.pipelines.KafkaPipeline',
]

# scrapy-kafka settings
SCRAPY_KAFKA_HOSTS = ['localhost:9092']
SCRAPY_KAFKA_SPIDER_CONSUMER_GROUP = 'scrapy-kafka'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'example (+http://www.yourdomain.com)'
