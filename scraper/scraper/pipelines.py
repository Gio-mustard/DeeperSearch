"""
This module contains a class that helps manage the output of the scraper.

The class is used to create the output directory, create the log file and write
the scraped items to it.
"""

import os
from datetime import datetime

class LogManager:
    """
    A class that helps manage the output of the scraper.

    This class is responsible for creating the output directory, creating the
    log file and writing the scraped items to it.
    """

    def __init__(self, output_dir="./scraper_results"):
        """
        Initializes the LogManager.

        Args:
            output_dir (str): The directory where the output will be stored.
        """
        self.output_dir = output_dir
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        """
        Ensures that the output directory exists.
        """
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def create_log_file(self):
        """
        Creates a log file with the current timestamp.

        Returns:
            str: The path of the created file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.output_dir, f"output_{timestamp}.txt")

    def write_log(self, file_path, item):
        """
        Writes the scraped item to the log file.

        Args:
            file_path (str): The path of the log file.
            item (dict): The scraped item.
        """
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"URL: {item['link']}\n")
            f.write(f"Title: {item['summarize']}\n")
            f.write(f"Content:\n{item['content']}\n")
            f.write("-" * 80 + "\n")


class PagePipeline:
    """
    Pipeline to process scraped pages
    
    This pipeline stores the scraped pages in a local log file
    and keeps track of the links that have been scraped.
    """

    responses:dict[str,dict[str,any]] = {}

    USE_LOGS = True
    @classmethod
    def from_responses(cls,link: str) -> str|None:
        """Retrieves the content from the responses for a given link
        
        Args:
            link (str): The link to retrieve the content from
        
        Returns:
            str|None: The content associated with the link, 
                None if the link is not found in the responses
        """
        return cls.responses.get(link)

    def __init__(self):
        self.log_manager = LogManager()
        if self.USE_LOGS:
            self.output_file = self.log_manager.create_log_file()

    def process_item(self, item, _):
        """
        Process an item by storing its content in the responses and logging it to the output file

        Args:
            item (dict): The item to process
            spider (Spider): The spider that yielded the item

        Returns:
            dict: The processed item
        """

        try:
            self.responses[item['link']] = {
                'summarize':item['summarize'],
                'content':item['content'],
                'link':item['link']
            }

            if self.USE_LOGS and hasattr(self, 'log_manager') and hasattr(self, 'output_file'):
                try:
                    self.log_manager.write_log(self.output_file, item)
                except (IOError, OSError) as e:
                    print(f"Error writing to log file: {e}")
            return item

        except (TypeError, ValueError) as e:
            print(f"Invalid item format: {e}")
            return item

        except AttributeError as e:
            print(f"Pipeline not properly initialized: {e}")
            return item
    