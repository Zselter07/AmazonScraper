from url_creator import create_product_url
from bs4 import BeautifulSoup
from utils.request import request
from utils import utils
from parser import Parser
import json, re
import validators

# product_url = create_product_url(product_id)

products_page_input = input("Enter url of the products page: ")
check_url = validators.url(products_page_input)
if check_url==True:
    url_products = request(products_page_input)
else:
    print("Invalid url")

my_parser = Parser()
product_ids = my_parser.parse_page(url_products) #get the list of the product IDs 

for product_id in product_ids:
    url_product = create_product_url(product_id)
    response_details = request(url_product)
    response_reviews = request('https://www.amazon.com/gp/customer-reviews/aj/private/reviewsGallery/get-data-for-reviews-image-gallery-for-asin?asin='+product_id)
    product_details = my_parser.parse_product(response_details)
    product_reviews = my_parser.parse_reviews(response_reviews)
    full_details = {
        'product_details': product_details, 
        'product_reviews': product_reviews
    }
    file_name = product_id + '.txt'
    with open(file_name, 'w') as f:
        json.dump(full_details, f, indent=4)



# print(my_parser.parse_product(r))
# print(my_parser.parse_reviews(r))
# with open('testing.txt', 'w') as f:
#     f.write(r.text)











# https://www.amazon.com/s?k=laptop&ref=nb_sb_noss_2
# https://www.amazon.com/s?k=iphone&ref=nb_sb_noss_2
# https://www.amazon.com/s?k=toys&ref=nb_sb_noss_2

# soup = BeautifulSoup(r.content, 'lxml')

# images_urls = []
# json_data = re.search("var obj = jQuery.parseJSON\('(.*)'\);", r.text).group(1)
# parsed_json = json.loads(json_data)

# print(Parser().parse_product(r))
