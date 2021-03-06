# from request import request
import requests

class FileDownloader:
    
    def download(self, path, url):
        img_data = requests.get(url).content

        with open(path, 'wb') as output:
            output.write(img_data)