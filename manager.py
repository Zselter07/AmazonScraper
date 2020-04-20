#TODO: Decouple the main manager

import json, re, os.path, sys, threading

from bs4 import BeautifulSoup
import tkinter as tk

from utils.resource_downloader import ResourceDownloader
from utils.image_resizer import resize_images
from utils.text_to_speech import TextToSpeech
from utils.resize_image_folder import PathUtils
from utils import text_from_product_reviews, utils, ffmpeg
from selenium_uploader import selenium_uploader
from selenium_affiliate_links import get_affiliate_links
from amazon import Amazon
from ffmpeg_tasks import create_final_video

def run(url: str):
    amazon = Amazon()
    resource_downloader = ResourceDownloader()

    products_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'products')
    os.makedirs(products_folder_path, exist_ok = True)

    product_ids = amazon.get_product_ids(url)

    ignored_ids_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ignored_asins.json')

    if not os.path.exists(ignored_ids_path):
        excluded_ids = []
        with open(ignored_ids_path, 'w') as f_not_exist:
            json.dump(excluded_ids, f_not_exist)

    with open(ignored_ids_path, 'r') as f:
        excluded_ids = json.load(f)

    for product_id in product_ids:
        if product_id not in excluded_ids:

            excluded_ids.append(product_id)
            with open(ignored_ids_path, 'w') as f_out:
                json.dump(excluded_ids, f_out)

            product_details, product_reviews = amazon.get_product(product_id)
            review_text = text_from_product_reviews.string_from_reviews(product_reviews)

            if review_text is not None:
        
                product_folder_path = os.path.join(products_folder_path, product_id)
                product_details_file_path = os.path.join(product_folder_path, 'product_details.json')
                resources_path = os.path.join(product_folder_path, 'resources')
                review_images_path = os.path.join(product_folder_path, 'review_images')
                images_paths = PathUtils.file_paths_from_folder(review_images_path)

                os.makedirs(resources_path, exist_ok = True)
                os.makedirs(review_images_path, exist_ok = True)

                with open(os.path.join(product_folder_path, 'review_text.txt'), 'w') as f:
                    f.write(review_text)

                with open(product_details_file_path, 'w') as f:
                    json.dump((product_details, product_reviews), f, indent=4)

                print('Create product_details and review_text')

                # resource_downloader.download_resources(product_details, resources_path)
                resource_downloader.download_review_resources(product_reviews, review_images_path)

                print('downloaded resources')     

                resize_images(images_paths)

                print('resized images')

                create_final_video(product_folder_path, review_text, review_images_path)

                print('Created final video')

                affiliate_link = get_affiliate_links(product_id)

                print('Scraped amazon affiliate link')

                youtube_video_title = product_details['title'][:100]
                youtube_video_description_list = product_details['features'][:4500]
                youtube_video_description = ' '.join(youtube_video_description_list)
                full_description = str(affiliate_link) + '\n' + youtube_video_description
                selenium_uploader(os.path.join(product_folder_path, 'final.mp4'), youtube_video_title, full_description, "amazon reviews, reviews, hones reviews, customer reviews,")

                print('Uploaded video to youtube and added all details')

## UI ### 

def get_entry():
    return e1.get()

def run_background():
    e1 = get_entry()
    t = threading.Thread(target=lambda: run(e1))
    t.daemon = True
    t.start()

def stop():
    master.destroy()


master = tk.Tk()
e1 = tk.Entry(master)
e1.grid(row=0, column=1)
tk.Label(master, text = "Enter URL").grid(row = 0, column = 0)
tk.Button(master, text = 'Run', command = lambda: run_background()).grid(row = 1, column = 0, columnspan = 2)
tk.Button(master, text = 'Quit', command = stop).grid(row = 2, column = 0)

master.mainloop()
