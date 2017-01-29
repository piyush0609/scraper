# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wikihowto.items import WikihowtoItem


class WikiCrawlerSpider(CrawlSpider):
    name = 'wiki_crawler'
    allowed_domains = ['wikihow.com']
    start_urls = ['http://www.wikihow.com/Title-Your-Work-of-Art']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = WikihowtoItem()

        item['url'] = response.url


        if(response.xpath('//*[@id="intro"]/h1/a/text()').extract()):
            item['page_title'] = response.xpath('//*[@id="intro"]/h1/a/text()').extract()[0]
        else:
            if(response.xpath('//h1/text()').extract()[0]):
                item['page_title'] = response.xpath('//h1/text()').extract()[0]
        #//*[@id="bodycontents"]/div[2]/h3/a
        x = response.xpath('//h3//*[contains(concat( " ", @class, " " ), concat( " ", "mw-headline", " " ))]//text()').extract()
        item['parts'] = {}
        for i in range(len(x)):
            item['parts'][x[i]] = []
            steps = response.xpath('//div[(@id = "steps_{0}")]//li//div[contains(concat( " ", @class, " " ), concat( " ", "step", " " ))]'.format(i+1))
            for j in steps:
                item['parts'][x[i]].append(j.xpath('b[@class="whb"]/text()').extract()[0] + ":" + j.xpath('text()').extract()[1])

        #item['parts'] = response.xpath('//h3//span[@class="mw-headline"]/@id').extract()
        #item['parts']['part_step'] = response.xpath('//*[@class="step"]')


        yield item
