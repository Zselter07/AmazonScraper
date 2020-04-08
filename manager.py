from url_creator import create_product_url
from bs4 import BeautifulSoup
from utils.request import request
from utils import utils
from parser import Parser
import json, re, validators, os.path, sys
import tkinter as tk
import threading


master = tk.Tk()

def main_manager():

    check_url = validators.url(e1.get())
    if check_url==True:
        url_products = request(e1.get())
    else:
        sys.exit('Url not valid')

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
        file_name = product_id + '.json'
        os.mkdir(os.path.join('/Users/macbook/github/AmazonScraper/Products', product_id))
        with open(os.path.join('/Users/macbook/github/AmazonScraper/Products', product_id, file_name), 'w') as f:
            json.dump(full_details, f, indent=4)

def download_background():
    t = threading.Thread(target=main_manager)
    t.daemon = True
    t.start()

def stop():
    master.destroy()

e1 = tk.Entry(master)
e1.grid(row=0, column=1)
tk.Label(master, text = "Enter URL").grid(row = 0, column = 0)
tk.Button(master, text = 'Run', command = download_background).grid(row = 1, column = 0, columnspan = 2)
tk.Button(master, text = 'Quit', command = stop).grid(row = 2, column = 0)

master.mainloop()
