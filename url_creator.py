from os import path

AMAZON_BASE_URL = 'https://www.amazon.com'

def create_product_url(product_id):
    return path.join(AMAZON_BASE_URL, 'dp', product_id)
