from os import path

AMAZON_BASE_URL = 'https://www.amazon.com/dp'

def creat_product_url(product_id):
    return path.join(AMAZON_BASE_URL, product_id)
