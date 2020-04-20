from os import path

class AmazonURLCreator:
    @staticmethod
    def create_product_url(asin):
        return path.join('https://www.amazon.com', 'dp', asin)

    @staticmethod
    def create_product_reviews_url(asin):
        return 'https://www.amazon.com/gp/customer-reviews/aj/private/reviewsGallery/get-data-for-reviews-image-gallery-for-asin?asin=' + asin