"""
@Giomustard
This module contains the item class for the web page that will be scraped.
"""

import scrapy

class PageItem(scrapy.Item):
    """
    The item class for the web page that will be scraped.
    
    Attributes:
        link (str): The link of the page.
        summarize (str): The summarize of the page.
        content (str): The content of the page.
    """
    link = scrapy.Field()
    summarize = scrapy.Field()
    content  = scrapy.Field()
