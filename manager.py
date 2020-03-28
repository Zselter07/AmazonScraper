from url_creator import create_product_url
from request import request
from bs4 import BeautifulSoup

product_url = create_product_url('B07THHQMHM')
r = request(product_url)
soup = BeautifulSoup(r.content, 'html.parser')
results = soup.find_all('span')
# print(results)
title = soup.find('span', attrs={'id':'productTitle'}).encode_contents().decode('utf-8').strip()
print('title:', title)
with open('testing.txt', 'w') as f:
    f.write(r.content.decode('utf-8'))
    
# print(soup.prettify())


# .decode('utf-8')
# print(results)