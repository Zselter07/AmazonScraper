from typing import List, Dict

import validators

from parser import Parser
from utils.request import request
from utils.url_creator import AmazonURLCreator as URLCreator

class Amazon:
    def __init__(self):
        self.parser = Parser()

    def get_product_ids_and_next_page(self, url: str) -> (List[str], str):
        if validators.url(url):
            response = request(url)

            return (self.parser.parse_products_page(response), self.parser.next_products_page(response))

        return None, None

    def get_product(self, product_id: str) -> (Dict, List):        
        response_details = request(URLCreator.create_product_url(product_id))
        try:
            product_details = self.parser.parse_product(response_details)
        except Exception as e:
            print(e)
            product_details = None

        response_reviews = request(URLCreator.create_product_reviews_url(product_id))
        try:
            product_reviews = self.parser.parse_reviews(response_reviews)
        except Exception as e:
            print(e)
            product_reviews = None

        return product_details, product_reviews

        