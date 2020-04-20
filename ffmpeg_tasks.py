  

def create_final_video(product_folder_path, review_text, review_images_path):
    import os

    from utils.text_to_speech import TextToSpeech
    from utils import ffmpeg

    text_into_speech = TextToSpeech()
    
        ### Text to speech

    audio_file_path = os.path.join(product_folder_path, 'audio.mp3')
    text_into_speech.text_to_audio(review_text, audio_file_path)

        ### Create Video From Images 

    video_file_path = os.path.join(product_folder_path, 'amazon_video.mp4')
    ffmpeg.create_video_from_images(review_images_path, video_file_path)

        ### Audio to Video 

    final_video_path = os.path.join(product_folder_path, 'final.mp4')
    ffmpeg.audio_to_video(video_file_path, audio_file_path, final_video_path)


# audio_file_path = os.path.join(product_folder_path, 'audio.mp3')
# text_into_speech.text_to_audio(review_text, audio_file_path)

#     ### Create Video From Images 
# video_file_path = os.path.join(product_folder_path, 'amazon_video.mp4')
# ffmpeg.create_video_from_images(review_images_path, video_file_path)

#     ### Audio to Video 
# final_video_path = os.path.join(product_folder_path, 'final.mp4')
# ffmpeg.audio_to_video(video_file_path, audio_file_path, final_video_path)

#     ### Upload to youtube with selenium