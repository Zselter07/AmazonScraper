import re, json
import html

from bs4 import BeautifulSoup

from utils import utils

class Parser():

    def parse_product(self, response):
        categories = []
        features = []
        images_urls = []
        video_urls = []
        price = None 
        
        soup = BeautifulSoup(response.content, 'lxml')
        json_data = re.search("var obj = jQuery.parseJSON\('(.*)'\);", response.text).group(1)
        parsed_json = json.loads(json_data)

        title = parsed_json['title']
        images = parsed_json['colorImages']
        videos = parsed_json['videos']
        
        feature_table_first = soup.find('div', id="feature-bullets", class_ = "a-section a-spacing-medium a-spacing-top-small")

        if feature_table_first is not None:
            table_for_features = feature_table_first.find('ul', class_ = "a-unordered-list a-vertical a-spacing-none")

            for li in table_for_features.find_all('li'):
                features.append(li.get_text().strip())
        
        elif feature_table_first is None:
            features = None

        categ_table_first = soup.find('div', id = 'wayfinding§-breadcrumbs_container')

        if categ_table_first is not None:
            table_for_categories = categ_table_first.find('ul', class_ ='a-unordered-list a-horizontal a-size-small')

            for li in table_for_categories.find_all("li"):
                category = li.get_text().strip()

            if category != '›':
                categories.append(category)
                
        elif categ_table_first is None:
            categories = None

        price_element = soup.find('span', id="priceblock_ourprice")

        if price_element is not None:
            price = price_element.get_text()

        table_for_product_info = soup.find('table', id="productDetails_detailBullets_sections1", class_="a-keyvalue prodDetTable")

        product_information_dict = {}
        if table_for_product_info is not None:
            for tr in table_for_product_info.find_all('tr'):
                key = tr.find('th').get_text().strip()

            if key not in ['Customer Reviews', 'Best Sellers Rank']:
                value = tr.find('td').get_text().strip()
                product_information_dict[key] = value

        for key, value in images.items():
            sub_images_urls = []

            for elem in value:
                if 'hiRes' in elem: 
                    sub_images_urls.append(elem['hiRes'])
            
            if len(sub_images_urls) > 0:
                images_urls.append(sub_images_urls)

        for url in videos:
            if 'url' in url:
                video_urls.append(url['url'])
            
        product_elements = {
            'title': title, 
            'price': price,
            'categories': categories,
            'features': features,
            'product information': product_information_dict,
            'images_url': images_urls,
            'videos_url': video_urls
            }

        return product_elements
    
    def parse_reviews(self, response):
        reviews_json = json.loads(response.text)
        image_urls = []
        reviews = []
        images = reviews_json['images']

        for image in images:
            if 'mediumImage' in image:
                image_urls.append(image['mediumImage'])

        for elem in images:
            if 'associatedReview' in elem:
                assoc_review = elem['associatedReview']
            if 'text' in assoc_review:
                review = assoc_review['text']
                review_beautify = html.unescape(review)
                reviews.append(review_beautify)
        
        review_elements = {
            'images': image_urls,
            'reviews': reviews
        }

        return review_elements

    def parse_page(self, response):   
        # response = 'https://www.amazon.com/gp/customer-reviews/aj/private/reviewsGallery/            get-data-for-reviews-image-gallery-for-asin?asin='
        asin_ids = []
        soup = BeautifulSoup(response.content, 'lxml')
        results = soup.find_all('span', class_="a-declarative")
        
        for elem in results:
            try:
                asin_id = utils.string_between(elem['data-a-popover'], 'asin=', '&')

                if asin_id is not None:
                    asin_ids.append(asin_id)
            except:
                pass
        
        return asin_ids