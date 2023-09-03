#!/usr/bin/env venv/bin/activate
"""Scrape products"""

from uuid import uuid4
import scrapy
from scrapy.spiders import logging
from scrapy.loader import ItemLoader
import json

from ecommerce_scrape.items import (
    Brand,
    Category,
    Comment,
    Product,
    ProductImage,
    ProductReview,
    User
)


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["www.konga.com", "www.api.konga.com"]
    page = 0
    pages = 0
    category = None
    brands = None

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
        self.brands = {}
        if not self.category:
            self.category = Category()
            self.category["name"] = response.css(
                "._1fce2_1jxDY li:nth-child(2) a::text").get()
            self.category["id"] = str(uuid4())
        product = Product()
        product["name"] = response.css('._24849_2Ymhg::text').get()
        product["price"] = response.css('._678e4_e6nqh::text').get()
        product["description"] = product_desc
        product["id"] = str(uuid4())
        product_images = response.css(".fd8e9_1qWnZ ._7fdb1_1W4TA").css("img")
        for i, product_info in enumerate(product_images):
            product_image = ProductImage()
            product_image["image_url"] = product_info.xpath("@src").get()
            product_image["alt_text"] = product_info.xpath("@alt").get()
            product_image["caption"] = product_info.xpath("@alt").get()
            product_image["order"] = i
            if not product.get("product_image"):
                product["product_image"] = product_image["image_url"]
            if product.get("images"):
                product["images"].append(product_image["image_url"])
            else:
                product["images"] = [product_image["image_url"]]

        if self.category.get("products"):
            self.category["products"].append(product["id"])
            product["category"] = self.category["id"]
        else:
            self.category["products"] = [product["id"]]
            product["category"] = self.category["id"]

        comment = Comment()
        user = User()
        review = ProductReview()
        brand_name = response.css("._71bb8_13C6j span::text").get()
        if brand_name:
            if brand_name not in self.brands:
                brand = Brand()
                brand["name"] = brand_name
                brand["id"] = str(uuid4())
                brand["products"] = [product["id"]]
                self.brands[brand_name.strip()] = brand
                product["brand"] = brand["id"]
            else:
                self.brands[brand_name]["products"].append(product["id"])
                product["brand"] = self.brands["id"]

        yield product
