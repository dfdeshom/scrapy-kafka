# -*- coding: utf-8 -*-
from scrapy_kafka.spiders import KafkaSpider
from example.items import DmozItem


class CustomKafkaSpider(KafkaSpider):
    name = "dmoz_kafka"
    allowed_domains = ["dmoz.org"]

    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            item = DmozItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item
