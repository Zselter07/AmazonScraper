def string_creator_from_review_texts(product_reviews, min_review_length = 50, max_review_length = 1000, max_total_text_length = 5000, min_total_text_length = 500):
    import os
    import json
    from langdetect import detect

    review_texts = []
    review_text_string = ''

    for product in product_reviews:
        
        if int(product['rating']) == 5 and len(product['text']) > min_review_length and len(product['text']) < max_review_length and detect(product['text']) == 'en':
            review_texts.append(product['text'])
        
        review_text_string = '.'.join(review_texts)

        if len(review_text_string) >= max_total_text_length:
            break
        
    if len(review_text_string) > min_total_text_length:

        return review_text_string
    
    return None
        # with open(os.path.join(folder_path, 'review_text.txt'), 'w') as f:
        #     f.write(review_text_string)
    