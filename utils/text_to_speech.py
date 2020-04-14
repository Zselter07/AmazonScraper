class TextToSpeech:
    def text_to_audio(self, text, folder_path):
        import os
        import pyttsx3

        engine = pyttsx3.init()
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.daniel.premium')
        engine.save_to_file(text=text,filename=os.path.join(folder_path, 'audio.mp3'))
        engine.runAndWait() 
