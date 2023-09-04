# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class EcommerceScrapePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if "price" in adapter:
            value = adapter.get("price")
            value = str(value).replace(",", "")
            adapter["price"] = float(value)
        # if item.__class__.__name__ == "Product":
        #     {"name": adapter.get("price"),
        #      "description": adapter.get("description")
        #      "brand_id"}
        #     storage.create("Product", )
        return item
