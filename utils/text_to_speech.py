class TextToSpeech:
    def text_to_audio(
        self,
        text: str,
        audio_path: str,
        speech_rate: int = 130 # words/minute
    ):
        import os
        import pyttsx3
        from . import ffmpeg
        from pathlib import Path

        audio_path = Path(audio_path)

        parent_dir = audio_path.parent
        extension = audio_path.suffix
        audio_path = str(audio_path)

        temp_file_base_name = '.__temp__'
        temp_path = str(Path.joinpath(parent_dir, temp_file_base_name + extension))

        engine = pyttsx3.init()
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.daniel.premium')
        engine.setProperty('rate', speech_rate)
        engine.save_to_file(text=text, filename=temp_path)
        engine.runAndWait() 

        ffmpeg.reencode_mp3(temp_path, audio_path)
        os.remove(temp_path)
    
    # def get_audio_duration(self, audio_path):
    #     from mutagen.mp3 import MP3
    #     from . import utils

    #     audio = MP3(audio_path)
    #     duration_int = round(audio.info.length)
    #     duration_formatted = utils.secondsToText(duration_int)

    #     return duration_formatted