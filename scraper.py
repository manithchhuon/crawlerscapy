import scrapy

class BrickSetSpider(scrapy.Spider):
    name = "cne_wtf"
    start_url = ['https://cne.wtf']
    def parse(self,response):
        SET_SELECTOR = ".entry-content"
        for brickset in response.css(SET_SELECTOR):
            