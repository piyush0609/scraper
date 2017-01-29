# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from brightnest.items import BrightnestItem
class BrightnestCrawlerSpider(CrawlSpider):
    name = 'brightnest_crawler'
    allowed_domains = ['brightnest.com']
    start_urls = ['http://brightnest.com/']

    rules = [
        Rule(LinkExtractor(),
             callback='parse_item', follow=True)
    ]

    def parse_item(self, response):
        item = BrightnestItem()

        url = response.url
        if('todos' in url):
            item['url'] = response.url
            # print(response.text)
            item['title'] = response.xpath(
                '//h1[@class="post_name"]/text()').extract()[0]
            item['reason'] = response.xpath(
                '//div[@class="info-header"]/div[@class="right"]/p/text()').extract()[0]
            item['img_urls'] = [response.xpath(
                '//div[@class="info-header"]/div[@class="left"]/img/@src').extract()[0]]

            steps = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "step-description", " " ))]//p')
            item['step'] = []
            print steps
            for step in steps:
                print step.xpath('b/text()').extract(), step.xpath('text()').extract()
                if(len(step.xpath('b/text()').extract())) and len(step.xpath('text()').extract()):
                    item['step'].append(step.xpath('b/text()').extract()[0] + " : " + step.xpath('text()').extract()[0])

            yield item
        if('posts' in url):
            item['url'] = response.url

            item['title'] = response.xpath(
                '//*[contains(concat( " ", @class, " " ), concat( " ", "post_name", " " ))]/text()').extract()

            #//*[contains(concat( " ", @class, " " ), concat( " ", "post_name", " " ))]
            item['reason'] = response.xpath(
                'div[@class="explore-post"]/p/span/text()').extract()
            x = response.xpath(
                '//*[contains(concat( " ", @class, " " ), concat( " ", "responsive-content", " " ))]/@src').extract()
            item['img_urls'] = x
            yield item
