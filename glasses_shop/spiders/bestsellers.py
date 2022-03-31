

from gc import callbacks
from math import prod
import scrapy


class BestsellersSpider(scrapy.Spider):
    name = 'bestsellers'
    # We're staying within the glassesshop.com domain for this small project.
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['http://www.glassesshop.com/bestsellers/']


    def parse(self, response):
        # Create an array of div objects, each being one product.
        product_list = response.xpath("//div[@id='product-lists']/div")
        # Loop through each product, extracting some data.
        for product in product_list:

            # div[3] contains one or more anchor tags with href pointing to link(s) of the image(s).
            # Thus I use .getall() to obtain an array of them.
            product_images = product.xpath(".//div[3]/a/@href").getall()
            # Get rid of "javascript:void(0);" entries
            product_images = [x for x in product_images if x != "javascript:void(0);"]

            # div[4] contains the other three pieces of data I want.
            product_data = product.xpath(".//div[4]")

            # product_data contains name, somewhere nested in there, in title tag of anchor.
            product_name = product_data.xpath(".//div[2]/div/div[1]/div/a[1]/@title").get()

            # product_data also contains link to the item's page.
            product_link = product_data.xpath(".//div[2]/div/div[1]/div/a[1]/@href").get()

            # Finally, product_data also contains price.
            product_price = product_data.xpath(".//div[2]/div/div[2]/div/div/span[1]/text()").get()

            yield {
                "name": product_name,
                "price": product_price,
                "link": product_link,
                "images": product_images
            }

        # Next, I want to recurse through this parse method until we're at the last page of products.
        # I can tell it's the last page when there is no "Next" button.
        next_link = response.xpath("//a[@rel='next']/@href").get()
        if next_link:
            # run parse again on the next page.
            yield scrapy.Request(url=next_link, callback=self.parse)

# OUTPUT IS STORED IN best_sellers_data.json
