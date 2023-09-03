# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from itemloaders.processors import Join, MapCompose
import scrapy
from w3lib.html import remove_tags, replace_entities


class Product(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    product_image = scrapy.Field()
    reviews = scrapy.Field()
    images = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()


class ProductImage(scrapy.Item):
    """Defines product images"""
    image_url = scrapy.Field()
    caption = scrapy.Field()
    alt_text = scrapy.Field()
    order = scrapy.Field()


class ProductReview(scrapy.Item):
    """Defines Product Review"""
    user_id = scrapy.Field()
    product_id = scrapy.Field()
    rating = scrapy.Field()


class Comment(scrapy.Item):
    """Comment for product Review"""
    user_id = scrapy.Field()
    product_id = scrapy.Field()
    content = scrapy.Field()


class User(scrapy.Item):
    """User Item"""
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    reviews = scrapy.Field()


class Category(scrapy.Item):
    """category item"""
    name = scrapy.Field()
    id = scrapy.Field()
    products = scrapy.Field()


class Brand(scrapy.Item):
    """Brand item"""
    id = scrapy.Field()
    name = scrapy.Field()
    products = scrapy.Field()
