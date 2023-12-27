#!/usr/bin/env venv/bin/activate
"""Scrape products"""

from uuid import uuid4
import scrapy
import json

from w3lib.html import remove_tags

from ecommerce_scrape.items import (
    Brand,
    Category,
    Product,
    ProductImage,
)


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["www.konga.com", "www.api.konga.com"]
    page = 0
    pages = 0

    def start_requests(self):
        """Starting point for request"""
        self.url = "https://api.konga.com/v1/graphql"
        self.headers = {
            "authority": "api.konga.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "dnt": "1",
            "origin": "https://www.konga.com",
            "pragma": "no-cache",
            "referer": "https://www.konga.com/",
            "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            "x-app-source": "kongavthree",
            "x-app-version": "2.0"
        }

        self.body = {
            "query": """
            {
                searchByStore(
                    search_term: [["category.category_id:5294"]],
                    numericFilters: [],
                    sortBy: "",
                    paginate: { page: %i, limit: 2000 },
                    store_id: 1
                ) {
                    pagination {
                        limit,
                        page,
                        total
                    },
                    products {
                        brand,
                        description,
                        name,
                        objectID,
                        original_price,
                        price,
                        sku,
                        url_key,
                        categories {
                            id,
                            name,
                            url_key,
                            position
                        },
                    }
                }
            }
            """ % (self.page)
        }
        yield scrapy.Request(
            url=self.url,
            method='POST',
            headers=self.headers,
            body=json.dumps(self.body)
        )

    def parse(self, response):
        """Parse start of request"""
        products_response = response.json().get('data').get('searchByStore')
        self.pages = products_response.get('pagination').get('total')

        for product in products_response.get("products"):
            url_key = product.get("url_key")

            if url_key:
                url = "https://www.konga.com/product/" + url_key
                yield scrapy.Request(
                    url=url,
                    method='GET',
                    headers=self.headers,
                    callback=self.product_parse,
                    cb_kwargs={"product_desc": product.get("description")}
                )
        else:
            if self.page < self.pages:
                self.page = self.page + 1
                self.body = {
                    "query": """
                    {
                        searchByStore(
                            search_term: [["category.category_id:5294"]],
                            numericFilters: [],
                            sortBy: "",
                            paginate: { page: %i, limit: 2000 },
                            store_id: 1
                        ) {
                            pagination {
                                limit,
                                page,
                                total
                            },
                            products {
                                brand,
                                description,
                                name,
                                objectID,
                                original_price,
                                price,
                                sku,
                                url_key,
                                categories {
                                    id,
                                    name,
                                    url_key,
                                    position
                                },
                            }
                        }
                    }
                    """ % (self.page)
                }
                yield scrapy.Request(
                    url=self.url,
                    headers=self.headers,
                    body=json.dumps(self.body),
                    method="POST",
                    callback=self.parse
                )

    def product_parse(self, response, product_desc):
        """Parse a product"""
        product = Product()
        product["name"] = response.css('._24849_2Ymhg::text').get()
        product["price"] = response.css('._678e4_e6nqh::text').get()
        product["description"] = product_desc
        product["id"] = str(uuid4())
        yield product
        product_images = response.css(".fd8e9_1qWnZ ._7fdb1_1W4TA").css("img")
        for i, product_info in enumerate(product_images):
            product_image = ProductImage()
            product_image["image_url"] = product_info.xpath("@src").get()
            product_image["alt_text"] = product_info.xpath("@alt").get()
            product_image["caption"] = product_info.xpath("@alt").get()
            product_image["order"] = i
            product_image["product"] = product["id"]
            yield product_image

        category = Category()
        category["name"] = response.css(
            "._1fce2_1jxDY li:nth-child(2) a::text").get()
        category["id"] = str(uuid4())
        category["product_id"] = product["id"]
        brand_name = response.css("._71bb8_13C6j span").get()
        if brand_name:
            brand = Brand()
            brand["name"] = remove_tags(brand_name).strip()
            brand["id"] = str(uuid4())
            brand["product"] = product["id"]
            yield brand
        yield category
