# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log,Request
from scrapy.pipelines.images import ImagesPipeline

class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        self.collection.update({'url': item['url']}, dict(item), upsert=True)
        log.msg("Question added to MongoDB database!",
                level=log.DEBUG, spider=spider)
        return item

class ImgPipeline(ImagesPipeline):
    def set_filename(self, response):
        return 'full/{0}.jpg'.format(response.meta['title'])

    def get_media_requests(self, item, info):
        for image_url in item['img_urls']:
            yield Request(image_url, meta={'title': item['title']})

    def get_images(self, response, request, info):
        for key, image, buf in super(ImgPipeline, self).get_images(response, request, info):
            print response.meta
            key = self.set_filename(response)
        yield key,image,buf
