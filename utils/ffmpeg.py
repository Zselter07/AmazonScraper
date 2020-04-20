from . import sh
import os

def reencode_mp3(path_in, path_out):
    sh.sh('ffmpeg -y -i ' + path_in + ' -codec:a libmp3lame -qscale:a 2 ' + path_out)

def create_video_from_images(input_folder, output_file_path, file_base_name = 'image',  file_extension = '.jpg'):
    sh.sh('ffmpeg -framerate 0.33 -start_number 001 -i ' + os.path.join(input_folder, file_base_name + '%03d' + file_extension) + ' -pix_fmt yuv420p ' + output_file_path)


    # sh.sh('ffmpeg -framerate 0.33 -start_number 001 -i /Users/macbook/github/AmazonScraper/products/B07RF1XD36/review_images/image%03d.jpg -pix_fmt yuv420p Users/macbook/github/AmazonScraper/products/B07RF1XD36/amazon_video_test.mp4

    # ffmpeg -framerate 0.33 -t 00:15:00 -start_number 001 -i /Users/macbook/github/AmazonScraper/products/B07RF1XD36/review_images/image%03d.jpg -pix_fmt yuv420p /Users/macbook/github/AmazonScraper/products/B07RF1XD36/amazon_video_test.mp4

def audio_to_video(input_video, input_audio, output_file):
    sh.sh('ffmpeg -i ' + input_video + ' -i ' + input_audio +  ' -codec copy -shortest ' + output_file)
    # ffmpeg -i video.mp4 -i audio.mp3 -codec copy -shortest output.mp4