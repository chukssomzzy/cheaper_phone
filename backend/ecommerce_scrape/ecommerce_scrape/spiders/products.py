#!/usr/bin/env venv/bin/activate
"""Scrape products"""

import scrapy
from scrapy_splash import SplashRequest
from scrapy.shell import inspect_response


script = """
function main(splash)
    splash:init_cookies(splash.args.cookies)
    assert(splash:go{
        splash.args.url,
        headers=splash.args.headers,
        http_method=splash.args.http_method,
        body=splash.args.body
    })
    assert(splash:wait(0.5))

    local product_card = splash:select_all("._7e903_3FsI6 .lazyloaded")
    local card_contents = {}
    local entries = nil
    local last_response = nil

    for _, card in ipairs(product_card) do
        assert(card:mouse_click())
        assert(splash:wait(0.5))
        card_contents[#card_contents + 1] = splash:html()
    end
    entries = splash:history()
    last_response = entries[#entries].response
    return {
        url = splash:url(),
        headers = last_response.headers,
        http_status = last_response.status,
        cookies = splash:get_cookies(),
        html = splash:html()
    }
end
"""


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["www.konga.com"]
    start_urls = ["https://www.konga.com"]

    def start_requests(self):
        """Starting point for request"""
        url = self.start_urls[0] + "/category/phones-tablets-5294"

        yield SplashRequest(
            url,
            self.parse, endpoint="execute",
            cache_args=['lua_source'],
            args={'lua_source': script}
        )

    def parse(self, response):
        inspect_response(response, self)
