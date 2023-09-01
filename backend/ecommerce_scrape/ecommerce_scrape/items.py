# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field(serializer=float)
    product_images = scrapy.Field()


class ProductImage(scrapy.Item):
    """Defines product images"""
    image_url = scrapy.Field()
    caption = scrapy.Field()
    alt_text = scrapy.Field()
    order = scrapy.Field(serializer=int)


class ProductReview(scrapy.Item):
    """Defines Product Review"""
    user_id = scrapy.Field()
    product_id = scrapy.Field()
    rating = scrapy.Field()
    brand_id = scrapy.Field()


class User(scrapy.Item):
    """User Item"""
    first_name = scrapy.Field()
    last_name = scrapy.Field()


class Category(scrapy.Item):
    """category item"""
    name = scrapy.Field()
