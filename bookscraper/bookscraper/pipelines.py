# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                if not value:
                    continue
                adapter[field_name] = value.strip()
        return item
    
import mysql.connector

class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'mybooks',
        )
        ## create a cursor, used to execute commands
        self.cur = self.conn.cursor()
        
        ## create books table
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS mybooks(
                title TEXT,
                product_type TEXT,
                price_excl_tax TEXT,
                price_incl_tax TEXT,
                tax TEXT,
                availability TEXT,
                number_of_reviews TEXT
            )
        """)


    def process_item(self, item, spider):
        self.cur.execute(""" insert into mybooks (
            title,
            product_type,
            price_excl_tax,
            price_incl_tax,
            tax,
            availability,
            number_of_reviews
            ) values (
                %s, %s, %s, %s, %s, %s, %s
                )""", (
            item["title"],
            item["product_type"],
            item["price_excl_tax"],
            item["price_incl_tax"],
            item["tax"],
            item["availability"],
            item["number_of_reviews"]
        ))

        ## Execute insert of data into database
        self.conn.commit()
        return item

    
    def close_spider(self, spider):
        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()
