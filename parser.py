import re, json, html

from bs4 import BeautifulSoup

from utils import utils

class Parser():

    def parse_product(self, response):
        categories = []
        features = []
        video_urls = []
        price = None
        
        soup = BeautifulSoup(response.content, 'lxml')
        try:
            json_data = re.search("var obj = jQuery.parseJSON\('(.*)'\);", response.text).group(1)
        except Exception:
            print(Exception)
            return None

        try:
            parsed_json = json.loads(json_data)
        except Exception as e:
            print(e)
            return None

        title = parsed_json['title']
        images = parsed_json
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

        image_details = {}

        if 'colorToAsin' in images and images['colorToAsin'] is not None:
            colors = images['colorToAsin']

            for color_name, color_dict in colors.items():
                # images_urls = []
                asin = color_dict['asin']
                image_details[asin] = {
                    'name' : color_name,
                    'image_urls' : []
                }
                
                images_by_color = images['colorImages'][color_name]

                for elem in images_by_color:
                    if 'hiRes' in elem: 
                        image_details[asin]['image_urls'].append(elem['hiRes'])

            for url in videos:
                if 'url' in url:
                    video_urls.append(url['url'])
            
        product_elements = {
            'title': title, 
            'price': price,
            'categories': categories,
            'features': features,
            'product information': product_information_dict,
            'images': image_details,
            'videos_url': video_urls
            }

        return product_elements
    
    def parse_reviews(self, response):
        # response = 'https://www.amazon.com/gp/customer-reviews/aj/private/reviewsGallery/get-data-for-reviews-image-gallery-for-asin?asin='
        try:
            reviews_json = json.loads(response.text)        
        except Exception as e:
            print(e)
            return None
        
        reviews = {} 
        details = reviews_json['images']

        for elem in details:
            try:
                author = elem['associatedReview']['author']['name']
                text = elem['associatedReview']['text']
                clean_text = utils.remove_html_tags(text).replace('  ', ' ')
                review_key = author

                if review_key in reviews:
                    review = reviews[review_key]
                else:
                    review = {
                        'author':author,
                        'text': clean_text,
                        'rating':elem['associatedReview']['overallRating'],
                        'image_urls':[]
                    }

                    if 'scores' in elem['associatedReview'] and 'helpfulVotes' in elem['associatedReview']['scores']:
                        review['upvotes'] = int(elem['associatedReview']['scores']['helpfulVotes'])
                    else:
                        review['upvotes'] = 0
                
                img_url = elem['mediumImage']
                review['image_urls'].append(img_url)

                reviews[review_key] = review     
            except:
                pass

        return sorted(list(reviews.values()), key=lambda k: k['upvotes'], reverse=True)

    def parse_products_page(self, response):   
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