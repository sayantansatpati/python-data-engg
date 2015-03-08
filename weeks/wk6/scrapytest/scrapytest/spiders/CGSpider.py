from __future__ import absolute_import

from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapytest.items import CraigslistSampleItem


class MySpider(Spider):
    name = "craig"
    allowed_domains = ["craigslist.org"]
    start_urls = ["http://sfbay.craigslist.org/search/cta"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.select("//span[@class='pl']")
        items = []
        for titles in titles:
            item = CraigslistSampleItem()
            item["title"] = titles.select("a/text()").extract()
            item["link"] = titles.select("a/@href").extract()
            items.append(item)
            print(item["title"] + item["link"])
        return items
