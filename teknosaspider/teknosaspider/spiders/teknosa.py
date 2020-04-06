# -*- coding: utf-8 -*-
import scrapy
from ..items import TeknosaspiderItem


class TeknosaSpider(scrapy.Spider):
    name = 'teknosa'
    allowed_domains = ['teknosa.com']
    start_urls = ['https://www.teknosa.com/notebook-laptop-c-1020101']
    main_domain = 'https://www.teknosa.com'

    def parse(self, response):
        all_product = response.css('.product-detail')

        product_href = all_product.css(' a::attr(href)')

        for urls in product_href:
            product_url = self.main_domain + urls.extract()

            yield scrapy.Request(product_url, callback=self.parse_product)

        next_page_href = response.css('.pagination-next a::attr(href)')
        next_page = self.main_domain + next_page_href.extract_first()

        yield scrapy.Request(next_page, callback=self.parse)

    def parse_product(self, response):
        items = TeknosaspiderItem()

        product_name = response.css('h1::text').extract_first()
        product_price = response.css('.product-options .font-size-fifth::text').extract_first().replace('\n\t\t\t\t', '')
        product_rate = response.css('.rating::text').extract_first().replace('\n                                        ', '')
        tech_detail_1 = response.css('.attrib::text').extract()
        tech_detail_2 = response.css('.table span:nth-child(1)::text').extract()

        items['product_name'] = product_name
        items['product_price'] = product_price
        items['product_rate'] = product_rate
        items['tech_detail_1'] = tech_detail_1
        items['tech_detail_2'] = tech_detail_2

        yield items
