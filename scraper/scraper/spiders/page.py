"""
@Giomustard
This module contains a Spider class for scraping web pages.
"""
from typing import Iterator
from scrapy import Request, Spider
from scraper.items import PageItem

class PageSpider(Spider):
    """
    A Scrapy spider that crawls web pages and extracts their content.

    This spider is designed to crawl multiple web pages, extract their content,
    and process it through a pipeline. It validates URLs before crawling and
    handles various response status codes and content validation.

    Attributes:
        name (str): The name of the spider.
        links (list): A list of URLs to crawl.
        custom_settings (dict): Custom settings for the spider, including pipeline configuration.
    """

    name = 'pageSpider'
    links = []
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.PagePipeline': 300,
        }
    }

    def __init__(self, links: tuple|list[str], *args, **kwargs):
        """
        Initializes the spider with a list of links to crawl.

        Args:
            links (tuple|list[str]): The URLs to crawl.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.set_links(links)

    def __check_links(self, links: tuple|list[str]) -> None:
        """
        Validates that the provided links are valid (either tuple or list of strings).

        Args:
            links (tuple|list[str]): The links to validate.

        Raises:
            TypeError: If links is not a tuple or list, or if any element is not a string.
        """
        if not isinstance(links, (tuple,list)):
            raise TypeError('Links must be a tuple or a list')

        if not all(isinstance(link, str) for link in links):
            raise TypeError('Links must be a tuple or a list of strings')

    def set_links(self, links: tuple|list[str]) -> None:
        """
        Sets the links to crawl after validation.

        Args:
            links (tuple|list[str]): The URLs to crawl.
        """
        self.__check_links(links)
        self.links = links

    def start_requests(self) -> Iterator[Request]:
        """
        Generates Request objects for each URL in the links list.

        Yields:
            Request: A Scrapy Request object for each URL to crawl.
        """
        for link in self.links:
            yield Request(link, self.parse)

    def __response_is_ok(self, response) -> bool:
        """
        Validates the response status and content.

        Args:
            response: The Scrapy response object.

        Returns:
            bool: True if the response is valid (status 200 and has content),
                  False otherwise.
        """
        if response.status != 200:
            self.logger.warning(f"""Failed to fetch {response.url}
                with status code {response.status}""")
            return False

        if not response.text:
            self.logger.warning(f"Empty content from {response.url}")
            return False

        return True

    def parse(self, response) -> Iterator[PageItem]:
        """
        Parses the response, extracts title and content, and yields a PageItem.

        Args:
            response: The Scrapy response object containing the page content.

        Returns:
            PageItem: A Scrapy item containing the extracted data.
        """
        if not self.__response_is_ok(response):
            print(("*"*15)+f" Failed to fetch {response.url}"+" *"*15)
            return
        print("*"*5,f"parsing => {response.url}","*"*5)
        title = (response.css('h1::text').get()
                    or response.css('title::text').get()
                    or "No title found")
        content = response.text
        if len(content) < 10:#Min of content
            self.logger.info(f"Content from {response.url} might be too short")
        yield PageItem(
            link=response.url,
            summarize=title,
            content=content
        )
