from url_creator import create_product_url
from bs4 import BeautifulSoup
from utils.request import request
from parser import Parser
import json, re, validators, os.path, sys
import tkinter as tk
import threading
from resource_downloader import ResourceDownloader
from utils.image_resizer import resize_image
from utils.text_to_speech import TextToSpeech
from utils.resize_image_folder import ImagePaths
from utils import sh, stringcreator, utils


master = tk.Tk()

def main_manager():

    check_url = validators.url(e1.get())
    if check_url==True:
        url_products = request(e1.get())
    else:
        sys.exit('Url not valid')

    my_parser = Parser()
    paths_for_images = ImagePaths()
    product_ids = my_parser.parse_page(url_products) #get the list of the product IDs 

    for product_id in product_ids:
        url_product = create_product_url(product_id)
        response_details = request(url_product)
        response_reviews = request('https://www.amazon.com/gp/customer-reviews/aj/private/reviewsGallery/get-data-for-reviews-image-gallery-for-asin?asin='+product_id)

        print('requested urls')

        product_details = my_parser.parse_product(response_details)
        product_reviews = my_parser.parse_reviews(response_reviews)
        
        if product_details is None or product_reviews is None:
            continue

        full_details = {
            'product_details': product_details,
            'product_reviews': product_reviews
        }

        print('created full details')
        product_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'products', product_id)
        product_details_file_path = os.path.join(product_folder_path, 'product_details.json')
        resources_path = os.path.join(product_folder_path, 'resources')
        review_images_path = os.path.join(product_folder_path, 'review_images')

        os.makedirs(resources_path, exist_ok = True)
        os.makedirs(review_images_path, exist_ok = True)

        with open(product_details_file_path, 'w') as f:
            json.dump(full_details, f, indent=4)

        downloader_obj = ResourceDownloader()
        # downloader_obj.download_resources(product_details, resources_path)
        downloader_obj.download_review_resources(product_reviews, review_images_path)

        print('started downloading')

        images_paths = paths_for_images.file_paths_from_folder(review_images_path)
        
        for image in images_paths:
            resize_image(image)

        print('resized images')

        sh.sh('ffmpeg -framerate 0.33 -start_number 001 -i ' + os.path.join(review_images_path, 'image%03d.jpg') + ' -pix_fmt yuv420p ' + os.path.join(product_folder_path, 'amazon_video.mp4'))

        full_review_text = stringcreator.string_creator_from_review_texts(product_reviews)

        if full_review_text is not None:

            with open(os.path.join(product_folder_path, 'review_text.txt'), 'w') as f:
                f.write(full_review_text)
            
            text_into_speech = TextToSpeech()
            text_into_speech.text_to_audio(full_review_text, product_folder_path)

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
