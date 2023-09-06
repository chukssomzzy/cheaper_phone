# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter.adapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.spiders import logging
from w3lib.html import replace_entities
from models import storage
from models.brands import Brand
from models.categories import Category
from models.product_images import ProductImage


class ImageScrapePipeline:
    """Process Images and store to db"""

    def process_item(self, item, spider):
        """Process images"""
        # save images to db
        adapter = ItemAdapter(item)
        if item.__class__.__name__ == "ProductImage":
            values = {"image_url": adapter.get("image_url"),
                      "caption": adapter.get("caption"),
                      "alt_text": adapter.get("alt_text"),
                      "order": adapter.get("order"),
                      "product_id": adapter.get("product")
                      }
            image = storage.session.query(ProductImage).filter_by(
                image_url=adapter["image_url"]).one_or_none()
            if not image:
                storage.create("ProductImage", **values)
            else:
                raise DropItem
        storage.save()
        storage.close()
        return item


class ProductScrapePipeline:
    """process and store product in a db"""

    def process_item(self, item, spider):
        """Process product and store"""
        adapter = ItemAdapter(item)
        if item.__class__.__name__ == "Product":
            # convert price to float
            if "price" in adapter:
                value = adapter.get("price")
                value = str(value).replace(",", "")
                adapter["price"] = float(value)
            values = {"name": adapter.get("name"),
                      "description": adapter.get("description"),
                      "price": adapter.get("price"), 'id': adapter.get("id")}
            storage.create("Product", **values)
        storage.save()
        storage.close()
        return item


class CategoryScrapePipeline:
    """Process PipeLine"""

    def process_item(self, item, spider):
        """Process Category"""
        adapter = ItemAdapter(item)
        if item.__class__.__name__ == "Category":
            # convert lower case
            if adapter.get("name"):
                adapter["name"] = str(adapter["name"]).lower()
            category = storage.session.query(
                Category).filter_by(name=adapter["name"]).one_or_none()
            if not category:
                values = {"name": adapter.get("name")}
                category = storage.create("Category", **values)
            product = adapter.get("product_id")
            if product and category:
                product = storage.get("Product", product)
                if product:
                    product.categories.append(category)
        storage.save()
        storage.close()
        return item


class BrandScrapePipeline:
    """Process Brand item"""

    def process_item(self, item, spider):
        """Process Brands"""
        adapter = ItemAdapter(item)
        if item.__class__.__name__ == "Brand":
            if adapter.get("name"):
                adapter["name"] = replace_entities(
                    str(adapter.get("name")).lower())
            # save brands
            values = {"name": adapter.get("name")}
            brand = storage.session.query(Brand).filter_by(
                name=adapter["name"]).one_or_none()
            if not brand:
                values = storage.create("Brand", **values)
            products = adapter.get("products")
            if brand and products:
                for product in products:
                    product = storage.get("Product", product)
                    if product:
                        brand.products.append(product)
                        product.brand_id = brand.id

        storage.save()
        storage.close()
        return item
