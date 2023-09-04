# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.spiders import logging
from models import storage


class EcommerceScrapePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # add product to category:
        if len(spider.category["products"]):
            for id in spider.category["products"]:
                product = self.storage.get("Product", id)
                self.category.append(product)
            storage.save()
            spider.category["products"] = []

        # save images to db

        if item.__class__.__name__ == "ProductImage":
            values = {"image_url": adapter.get("image_url"),
                      "caption": adapter.get("caption"),
                      "alt_text": adapter.get("alt_text"),
                      "order": adapter.get("order")}
            values = self.storage.create("ProductImage", **values)
            storage.save()

        # Save categories
        if item.__class__.__name__ == "Category":
            if adapter.get("name") not in spider.categories_name:
                values = {"name": adapter.get("name")}
                category = self.storage.create("Category", **values)
                storage.save()
                if category:
                    spider.category["id"] = category.id
                    self.category = category

        # convert price to float
        if "price" in adapter:
            value = adapter.get("price")
            value = str(value).replace(",", "")
            adapter["price"] = float(value)

        # save a product
        if item.__class__.__name__ == "Product":
            values = {"name": adapter.get("price"),
                      "description": adapter.get("description"),
                      "brand_id": adapter.get("brand"),
                      "product_images": adapter.get("product_image")}
            values = storage.create("Product", **values)
            storage.save()
            # add more related images to product
            if values:
                images = item.get("images")
                for image in images:
                    values.images.append(self.storage.get(
                        "ProductImage", image, "image_url"))
                storage.save()

        # save brands
        if item.__class__.__name__ == "Brand":
            values = {"name": adapter.get("name")}
            values = self.storage.create("Brand", **values)
            self.storage.save()
            products = adapter.get("products")
            if values and products:
                for product in products:
                    values.products.append(
                        self.storage.get("Product", product))
                self.storage.save()
        self.storage.close()
        return item

    def open_spider(self, spider):
        """Open statement for a spider"""
        self.storage = storage
        categories = storage.all("Category")
        spider.categories_name = []
        for category in categories.values():
            spider.categories_name.append(category.name)

    def close_spider(self, spider):
        """Close a spider"""
        self.storage.save()
        self.storage.close()
