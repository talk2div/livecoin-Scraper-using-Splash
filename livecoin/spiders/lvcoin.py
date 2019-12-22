# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class LvcoinSpider(scrapy.Spider):
    name = 'lvcoin'
    allowed_domains = ['www.livecoin.net/en']

    script = """
        function main(splash, args)
            splash:set_user_agent("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36")
            splash.private_mode_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(1))
            rur_btn = assert(splash:select_all(".filterPanelItem___2z5Gb"))
            rur_btn[6]:mouse_click()
            splash:wait(1)
            btn = assert(splash:select(".button-red"))
            btn:mouse_click()
            assert(splash:wait(1))
            splash:set_viewport_full()
            return splash:html()
        end
    """
    def start_requests(self):
        yield SplashRequest(url='http://www.livecoin.net/en',callback=self.parse,endpoint="execute",args={
            'lua_source':self.script,
        })
    def parse(self, response):
        row = response.xpath('//div[contains(@class,"ReactVirtualized__Table__row tableRow___3EtiS ")]')
        for each_row in row:
            yield {
                'name': each_row.xpath('.//div[1]/div/text()').get(),
                'volume(24h)':  each_row.xpath('.//div[2]/span/text()').get(),
                'last Price': each_row.xpath('.//div[3]/span/text()').get()
            }