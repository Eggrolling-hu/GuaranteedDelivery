from scrapy.selector import Selector
from pathlib import Path

import scrapy
import time
import os

from wiki.items import ContentItem


class WikiSpider(scrapy.Spider):
    name = "wiki"
    n, max_n = 0, 20

    def start_requests(self):
        urls = [
            "https://zh.wikipedia.org/wiki/Category:%E9%87%91%E8%9E%8D",  # 金融
        ]
        for url in urls:
            if 'Category:' in url:
                yield scrapy.Request(url, callback=self.parse_category)
            else:
                yield scrapy.Request(url, callback=self.parse_content)

    def is_exceed_max_requests(self):
        self.n += 1
        if self.n <= self.max_n:
            return False
        return True

    def parse_category(self, response):
        if self.is_exceed_max_requests():
            return
        url_candidates_set = set()
        selector = Selector(response)
        contents = selector.xpath("//div[@id='content']")

        urls = contents.xpath(
            "//div[@class='mw-category-generated']//a/@href").extract()
        # 百科页面有许多超链接是锚链接，需要过滤掉
        for url in urls:
            # if filter(url):  # 分类请求中过滤掉一些不符合的请求（例如明显包含游戏的关键词都不要爬取）
            #     continue
            if '/wiki' in url and 'https://zh.wikipedia.org' not in url:
                if ':' not in url or (':' in url and 'Category:' in url):
                    url_candidates_set.add('https://zh.wikipedia.org' + url)

        print(f"To add {len(url_candidates_set)} urls")

        for url in url_candidates_set:
            if 'Category:' in url:
                yield scrapy.Request(url, callback=self.parse_category)
            else:
                yield scrapy.Request(url, callback=self.parse_content)

    def parse_content(self, response):
        if self.is_exceed_max_requests():
            return
        # filename = f"content-{self.n}.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")

        counselor_item = ContentItem()
        sel = Selector(response)
        search = sel.xpath("//div[@id='content']")
        content_entity = search.xpath(
            "//h1[@id='firstHeading']/span[@class='mw-page-title-main']/text()").extract_first()
        content_page = search.xpath(
            "//div[@id='bodyContent']//div[@id='mw-content-text']//div[@class='mw-parser-output']").extract_first()  # 将带有html的标签的整个数据拿下，后期做处理
        cates = search.xpath("//div[@id='catlinks']//ul//a/text()").extract()

        text_content_list = search.xpath(
            '//div[@class="mw-parser-output"]//p//text()').extract()
        text_content = " ".join(text_content_list).strip()
        # text_content = ""

        counselor_item['content_entity'] = content_entity if content_entity else self.n
        counselor_item['category'] = '\t'.join(cates)
        counselor_item['time'] = str(time.time())
        counselor_item['url'] = response.url
        counselor_item['text'] = text_content
        counselor_item['content'] = str(content_page)

        print("1111111,{}".format(counselor_item))

        return counselor_item
