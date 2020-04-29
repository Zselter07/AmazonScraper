import json, re, os.path, sys, threading, random, time
from datetime import datetime

from bs4 import BeautifulSoup
import tkinter as tk

from utils.resource_downloader import ResourceDownloader
from utils.image_resizer import resize_images
from utils.text_to_speech import TextToSpeech
from utils.url_creator import AmazonURLCreator
from utils import text_from_product_reviews, utils, ffmpeg
from utils import sh
from selenium_uploader import upload
from selenium_affiliate_links import get_affiliate_links
from amazon import Amazon
from ffmpeg_tasks import create_final_video

def run(
    url:str,
    host:str = None, 
    port:int = None,
    max_videos:int = 45
) -> int:
    uploaded_videos_count = 0
    amazon = Amazon()
    url_creator = AmazonURLCreator()
    resource_downloader = ResourceDownloader()
    products_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'products')
    os.makedirs(products_folder_path, exist_ok = True)
    next_page_url = None

    ignored_ids_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ignored_asins.json')

    if not os.path.exists(ignored_ids_path):
        excluded_ids = []
        with open(ignored_ids_path, 'w') as ignored_path_not_exist:
            json.dump(excluded_ids, ignored_path_not_exist)

    with open(ignored_ids_path, 'r') as f:
        excluded_ids = json.load(f)
 
    while True:
        if next_page_url is not None:
            url = next_page_url

        product_ids, next_page_param = amazon.get_product_ids_and_next_page(url)

        for product_id in product_ids:
            if product_id not in excluded_ids:

                product_details, product_reviews = amazon.get_product(product_id)
                
                if 'associated_asins' in product_details and product_details['associated_asins'] is not None:
                    for associated_asin in product_details['associated_asins']:
                        excluded_ids.append(associated_asin)
                        
                excluded_ids.append(product_id)

                with open(ignored_ids_path, 'w') as f_out:
                    json.dump(excluded_ids, f_out)
                
                min_review_len_minutes = 1
                max_review_len_minutes = 5
                words_per_minute = 130
                
                review_text = text_from_product_reviews.string_from_reviews(
                    product_reviews,
                    min_total_text_length=min_review_len_minutes * words_per_minute,
                    max_total_text_length=max_review_len_minutes * words_per_minute
                )

                if review_text is not None and product_details is not None:
                    print('Creating product_details and review_text')

                    product_folder_path = os.path.join(products_folder_path, product_id)
                    product_details_file_path = os.path.join(product_folder_path, 'product_details.json')
                    resources_path = os.path.join(product_folder_path, 'resources')
                    review_images_path = os.path.join(product_folder_path, 'review_images')

                    os.makedirs(resources_path, exist_ok = True)
                    os.makedirs(review_images_path, exist_ok = True)

                    with open(os.path.join(product_folder_path, 'review_text.txt'), 'w') as f:
                        f.write(review_text)

                    with open(product_details_file_path, 'w') as f:
                        json.dump({
                            'product_details':product_details,
                            'product_reviews':product_reviews
                            }, f, indent=4)

                    print('downloading resources')

                    # resource_downloader.download_resources(product_details, resources_path)
                    resource_downloader.download_review_resources(product_reviews, review_images_path)

                    print('resizing images')

                    resize_images(review_images_path)

                    print('Creating final video')

                    create_final_video(product_folder_path, review_text, review_images_path)
                    
                    if os.path.exists(os.path.join(product_folder_path, 'final.mp4')):
                        print('Created final video')

                        try:
                            affiliate_link = get_affiliate_links(product_id)

                            print('Scraped amazon affiliate link')

                            youtube_video_title = product_details['title'][:90] + ' review' 
                            title_formattted = BeautifulSoup(youtube_video_title, "lxml").text.replace('\\', '/')
                            youtube_video_description_list = product_details['features'][:4500]
                            youtube_video_description = ' '.join(youtube_video_description_list)
                            full_description = 'BUY IT ON SALE ➡️  ' + str(affiliate_link) + '\n\n\n' + youtube_video_description
                            upload(os.path.join(product_folder_path, 'final.mp4'), title_formattted, full_description, "amazon reviews, reviews, honest reviews, customer reviews,", host=host, port=port)

                            print('Uploaded video to youtube and added all details')
                            
                            uploaded_videos_count += 1

                            if uploaded_videos_count == max_videos:
                                return uploaded_videos_count

                        except Exception as e:
                            print(e)
                    else:
                        print('Could not create final video')
        
        if next_page_param == None:
            return uploaded_videos_count

        next_page_url = url_creator.create_next_page_url(next_page_param)

try:
    import shutil

    shutil.rmtree(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'products'), )
except:
    pass

MAX_VIDEOS_PER_DAY = 45
urls = [
    'https://www.amazon.com/s?rh=n%3A565098%2Cp_72%3A4-&pf_rd_i=565098&pf_rd_p=76e296ad-5413-5bf6-af6f-01baaf1f131b&pf_rd_r=1PKH0MDTDS851FVQ3PYC&pf_rd_s=merchandised-search-11&pf_rd_t=BROWSE&refresh=1',
 
    'https://www.amazon.com/s?bbn=493964&rh=n%3A172282%2Cn%3A%21493964%2Cn%3A281407%2Cp_n_shipping_option-bin%3A3242350011&dc&fst=as%3Aoff&pf_rd_i=16225009011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=82d03e2f-30e3-48bf-a811-d3d2a6628949&pf_rd_r=3BN31PSJ01Y9S1FK3HZA&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1486423355&rnid=493964&ref=s9_acss_bw_cts_AEElectr_T1_w', 

    'https://www.amazon.com/s?bbn=493964&rh=n%3A172282%2Cn%3A%21493964%2Cn%3A502394%2Cp_n_shipping_option-bin%3A3242350011&dc&fst=as%3Aoff&pf_rd_i=16225009011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=82d03e2f-30e3-48bf-a811-d3d2a6628949&pf_rd_r=3BN31PSJ01Y9S1FK3HZA&pf_rd_s=merchandised-search-4&pf_rd_t=101&qid=1486423355&qid=1486423355&rnid=493964&rnid=493964%2Fs%2Fref%3Dsr_nr_n_1%3Ffst%3Das%3Aoff&ref=s9_acss_bw_cts_AEElectr_T2_w',
    
    'https://www.amazon.com/s?rh=n%3A1232597011%2Cp_72%3A4-&pf_rd_i=1232597011&pf_rd_p=c7366b1b-7311-5285-9ba2-8b5be038d4b2&pf_rd_r=VEZE6P873A1ZWP67JAH8&pf_rd_s=merchandised-search-11&pf_rd_t=BROWSE&ref=Oct_s9_apbd_otopr_hd_bw_b1LPqmx_S',

    'https://www.amazon.com/s?rh=n%3A1292115011%2Cp_72%3A4-&pf_rd_i=1292115011&pf_rd_p=cdc23760-bcad-51dd-89a5-59f1c87ba3c4&pf_rd_r=95QYANQC0QH8MQA9ZNDM&pf_rd_s=merchandised-search-11&pf_rd_t=BROWSE&ref=Oct_s9_apbd_otopr_hd_bw_b1PRa8h_S'
]

videos_counter_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'videos_counter.json')

try:
    with open(videos_counter_path, 'r') as f:
        number_of_videos_by_day = json.load(f)
except:
    number_of_videos_by_day = {
        'day':-1,
        'number_of_videos': 0
    }

while True:
    today = datetime.today().day

    if number_of_videos_by_day['day'] != today:
        number_of_videos_by_day['number_of_videos'] = 0 
        number_of_videos_by_day['day'] = today

        with open(videos_counter_path, 'w') as f:
            json.dump(number_of_videos_by_day, f, indent=4) 
    
    if number_of_videos_by_day['number_of_videos'] < MAX_VIDEOS_PER_DAY:
        uploaded_videos_count = run(
            random.choice(urls), 
            host='199.47.121.3', 
            port=24826,
            max_videos=MAX_VIDEOS_PER_DAY-number_of_videos_by_day['number_of_videos']
        )

        number_of_videos_by_day['number_of_videos'] += uploaded_videos_count

        with open(videos_counter_path, 'w') as f:
            json.dump(number_of_videos_by_day, f, indent=4)
    
    print('uploaded maximum amount for today')
    time.sleep(15)



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





# def login(id, url, host, port):
#     from utils.selenium_wrapper.Selenium import Selenium

#     browser = Selenium(id, host = host, port = port)
#     browser.driver.get(url)
#     input('log in and enter: ')
#     browser.driver.get(url)
#     time.sleep(1)
#     browser.save_cookies()
#     time.sleep(2)
#     browser.driver.quit()

# login('youtube', 'https://www.youtube.com/', '199.47.121.3', 24826)
# login('amazon', 'https://affiliate-program.amazon.com/', None, None)
# exit(0)