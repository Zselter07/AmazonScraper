import json, re, os.path, sys, threading, random

from bs4 import BeautifulSoup
import tkinter as tk

from utils.resource_downloader import ResourceDownloader
from utils.image_resizer import resize_images
from utils.text_to_speech import TextToSpeech
from utils.resize_image_folder import PathUtils
from utils.url_creator import AmazonURLCreator
from utils import text_from_product_reviews, utils, ffmpeg
from selenium_uploader import upload
from selenium_affiliate_links import get_affiliate_links
from amazon import Amazon
from ffmpeg_tasks import create_final_video

def run(
    url:str, 
    host:str=None, 
    port:int=None
):
    video_counter = 0
    amazon = Amazon()
    create_next_url = AmazonURLCreator()
    resource_downloader = ResourceDownloader()
    products_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'products')
    os.makedirs(products_folder_path, exist_ok = True)
    next_page_url = None

    while True:
        if next_page_url is not None:
            url = next_page_url

        product_ids, next_page_param = amazon.get_product_ids_and_next_page(url)
        next_page_url = create_next_url.create_next_page_url(next_page_param)

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

                    print('Creating product_details and review_text')

                    # resource_downloader.download_resources(product_details, resources_path)
                    resource_downloader.download_review_resources(product_reviews, review_images_path)

                    print('downloaded resources')     

                    resize_images(images_paths)

                    print('resized images')

                    create_final_video(product_folder_path, review_text, review_images_path)
                    
                    if os.path.exists(os.path.join(product_folder_path, 'final.mp4')):

                        print('Created final video')

                        affiliate_link = get_affiliate_links(product_id)

                        print('Scraped amazon affiliate link')

                        youtube_video_title = product_details['title'][:90] + ' review' 
                        title_formattted = BeautifulSoup(youtube_video_title, "lxml").text.replace('\\', '/')
                        youtube_video_description_list = product_details['features'][:4500]
                        youtube_video_description = ' '.join(youtube_video_description_list)
                        full_description = str(affiliate_link) + '\n' + youtube_video_description
                        upload(os.path.join(product_folder_path, 'final.mp4'), title_formattted, full_description, "amazon reviews, reviews, honest reviews, customer reviews,", host=host, port=port)

                        print('Uploaded video to youtube and added all details')
                        video_counter += 1 

                        if video_counter == 45:
                            exit(0)
                            print('uploaded 45 videos')

urls = [
    'https://www.amazon.com/s?rh=n%3A565098%2Cp_72%3A4-&pf_rd_i=565098&pf_rd_p=76e296ad-5413-5bf6-af6f-01baaf1f131b&pf_rd_r=1PKH0MDTDS851FVQ3PYC&pf_rd_s=merchandised-search-11&pf_rd_t=BROWSE&refresh=1',
 
    'https://www.amazon.com/s?bbn=493964&rh=n%3A172282%2Cn%3A%21493964%2Cn%3A281407%2Cp_n_shipping_option-bin%3A3242350011&dc&fst=as%3Aoff&pf_rd_i=16225009011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=82d03e2f-30e3-48bf-a811-d3d2a6628949&pf_rd_r=3BN31PSJ01Y9S1FK3HZA&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1486423355&rnid=493964&ref=s9_acss_bw_cts_AEElectr_T1_w', 

    'https://www.amazon.com/s?bbn=493964&rh=n%3A172282%2Cn%3A%21493964%2Cn%3A502394%2Cp_n_shipping_option-bin%3A3242350011&dc&fst=as%3Aoff&pf_rd_i=16225009011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=82d03e2f-30e3-48bf-a811-d3d2a6628949&pf_rd_r=3BN31PSJ01Y9S1FK3HZA&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1486423355&qid=1486423355&rnid=493964&rnid=493964%2Fs%2Fref%3Dsr_nr_n_1%3Ffst%3Das%3Aoff&ref=s9_acss_bw_cts_AEElectr_T2_w',
    
    'https://www.amazon.com/s?rh=n%3A1232597011%2Cp_72%3A4-&pf_rd_i=1232597011&pf_rd_p=c7366b1b-7311-5285-9ba2-8b5be038d4b2&pf_rd_r=VEZE6P873A1ZWP67JAH8&pf_rd_s=merchandised-search-11&pf_rd_t=BROWSE&ref=Oct_s9_apbd_otopr_hd_bw_b1LPqmx_S',

    'https://www.amazon.com/s?rh=n%3A1292115011%2Cp_72%3A4-&pf_rd_i=1292115011&pf_rd_p=cdc23760-bcad-51dd-89a5-59f1c87ba3c4&pf_rd_r=95QYANQC0QH8MQA9ZNDM&pf_rd_s=merchandised-search-11&pf_rd_t=BROWSE&ref=Oct_s9_apbd_otopr_hd_bw_b1PRa8h_S'
]

while True:
    run(random.choice(urls), host='199.47.121.3', port=24826)








## UI ### 

# def get_entry():
#     return e1.get()

# def run_background():
#     e1 = get_entry()
#     t = threading.Thread(target=lambda: run(e1))
#     t.daemon = True
#     t.start()

# def stop():
#     master.destroy()


# master = tk.Tk()
# e1 = tk.Entry(master)
# e1.grid(row=0, column=1)
# tk.Label(master, text = "Enter URL").grid(row = 0, column = 0)
# tk.Button(master, text = 'Run', command = lambda: run_background()).grid(row = 1, column = 0, columnspan = 2)
# tk.Button(master, text = 'Quit', command = stop).grid(row = 2, column = 0)

# master.mainloop()

