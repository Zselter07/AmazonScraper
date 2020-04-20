from utils.downloader import FileDownloader
import os 

class ResourceDownloader:

    def __init__(self):
        self.downloader = FileDownloader()

    def download_resources(self, json_details, folder_path):
        image_urls = json_details['images']
        counter = 0

        for video_url in json_details['videos_url']:
                counter += 1
                video_extension = video_url.split('.')[-1]
                video_resource_name = 'video' + str(counter) + '.' + video_extension
                self.downloader.download(os.path.join(folder_path, video_resource_name), video_url)

        for image in image_urls.values():
            urls = image['image_urls']

            for url in urls:
                splitted_url = url.split('/')[-1].split('.')
                resource_name = splitted_url[0] + '.' + splitted_url[-1]
                self.downloader.download(os.path.join(folder_path, resource_name), url)
    
    def download_review_resources(self, json_details, folder_path):
        # downloader = FileDownloader()
        counter = 0

        for review_detail in json_details:

            if review_detail['rating'] == 5:

                for image in review_detail['image_urls']:
                    counter += 1 
                    extension = image.split('.')
                    image_name = 'image' + str(counter).zfill(3) + '.' + extension[-1]
                    self.downloader.download(os.path.join(folder_path, image_name), image)

