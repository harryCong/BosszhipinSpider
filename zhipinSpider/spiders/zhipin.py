# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from zhipinSpider.items import ZhipinspiderItem
from scrapy_redis.spiders import RedisCrawlSpider

class ZhipinSpider(RedisCrawlSpider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    # start_urls = ['https://www.zhipin.com/c101010100-p100109/']
    redis_key = "zhipin:start_urls"

    rules = (
        Rule(LinkExtractor(allow=r'page=\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # print(response.url)
        job_url_list = response.xpath("//h3//a/@href").extract()
        for job_url in job_url_list:
            url = 'https://www.zhipin.com/' + job_url

            yield scrapy.Request(url,callback=self.parse_next)

    def parse_next(self,response):
        item = ZhipinspiderItem()

        item['job'] = response.xpath('//div[@class="name"]/h1/text()').extract_first()
        item['salary'] = response.xpath('//div[@class="name"]/span[@class="badge"]/text()').extract_first()
        item['company_name'] = response.xpath('//h3[@class="name"]/a/text()').extract_first()
        item['address'] = response.xpath('//div[@class="location-address"]/text()').extract_first()
        item['require'] = "".join(response.xpath('//div[@class="info-primary"]/p[1]/text()').extract()[1:3])
        item['company_size'] = " ".join(response.xpath("//div[@class='info-company']//p/text()").extract())
        item['job_info'] = response.xpath("//div[@class='job-sec']//div[@class='text']//text()").extract_first()
        item['company_info'] = response.xpath("//div[@class='job-sec company-info']//div[@class='text']//text()").extract_first()

        yield item