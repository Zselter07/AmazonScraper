import os.path

def url_creator(product_id):
    url = 'https://www.amazon.com'
    return os.path.join(url, product_id)
