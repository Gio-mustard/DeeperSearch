"""
Gio mustard
    A simple scrapper module to crawl a list of links and save the results in a pipeline.
"""
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scraper.pipelines import PagePipeline
from scraper.spiders.page import PageSpider

class Scrapper: # pylint: disable=too-few-public-methods
    """
    The class for crawl any web page and save the results in a pipeline.
    """
    def __init__(self, show_logs=False,callback:callable=lambda _:...):
        self.__process = CrawlerProcess(self.__get_settings(show_logs))
        deferred =  self.__process.join()
        deferred.addCallback(callback) # * This callback is called when a start method is end. pylint: disable=no-member

    def __get_settings(self, show_logs) -> dict:
        """
        Return the settings for the crawler process. If show_logs is false,
        disable the logs for the crawl process.
        """
        settings = get_project_settings()
        settings.set('LOG_ENABLED', show_logs)
        return settings

    def __group_links(self, links: list[str],items_per_group:int=1000) -> tuple[list[str]]:
        return tuple(links[i:i + items_per_group] for i in range(0, len(links), items_per_group))


    def start(self,links: list[str])-> tuple[str]:
        """
        Start the crawl process.

        Args:
            links (list[str]): The links to crawl.

        Returns:
            tuple[str]: The results of the crawl.
        """
        grouped_links = self.__group_links(links , items_per_group=1000)

        for group in grouped_links:
            self.__process.crawl(PageSpider, links=group)
        self.__process.start()
        return tuple(PagePipeline.from_responses(link) for link in links)

if __name__ == '__main__':
    def finish_crawl(argument):
        """
        This is a callback function that is called when the crawl is finished.
        
        Args:
            argument (str): An argument passed to this function.
        
        Returns:
            None
        """
        print(f"---- Crawl completed si que si {argument} ----")
    scrapper = Scrapper(show_logs=False,callback=finish_crawl)
    links_to_crawl = [
        "https://supermaven.com/",

        "https://docs.scrapy.org/en/latest/topics/api.html#module-scrapy.spiderloader",
        # "http://www.scielo.org.co/scielo.php?pid=S0121-11292015000100006&script=sci_arttext"
        ]
    result = scrapper.start(links_to_crawl)

    print("-"*5,(f"{result}"[0:20]),"...")
