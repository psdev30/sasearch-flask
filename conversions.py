from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment
import speech_recognition as sr
import os

clip_directory = 'C:/Users/psjuk/PyCharmProjects/SASearch-backend/clips_library/'


class Conversions:

    # converts mp4 to mp3
    @staticmethod
    def convert_to_mp3(file_name):
        mp4 = 'clips_library/' + file_name + '.mp4'
        mp3 = 'clips_library/' + file_name + '.mp3'
        wav = 'clips_library/' + file_name + '.wav'
        video_clip = VideoFileClip(mp4)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(mp3)
        audio_clip.close()
        video_clip.close()

        return mp3, wav

    # converts mp3 to wav
    @staticmethod
    def convert_to_wav(mp3, wav):
        sound = AudioSegment.from_mp3(mp3)
        sound.export(wav, format="wav")
        return

    # speech to text conversion
    @staticmethod
    def extract_text(wav, file_name):
        r = sr.Recognizer()
        with sr.WavFile(os.path.abspath(wav)) as source:
            try:
                audio = r.record(source)
                name = file_name.title()
                short_path = file_name + '.mp4'
                text = r.recognize_google(audio)

                if '_' in file_name:
                    name = name.replace('_', ' ')
                return name, short_path, text

            except:
                return name, short_path, 'N/A ' + name

    # remove mp4 from file directory
    @staticmethod
    def remove_files():
        for file in os.listdir(clip_directory):
            os.remove('clips_library/' + file + '.mp4')
            os.remove('clips_library/' + file + '.mp3')
            os.remove('clips_library/' + file + '.wav')

    # remove mp3 + wav from file directory
    @staticmethod
    def remove_mp3_wav():
        for file in os.listdir(clip_directory):
            if 'mp3' in file or 'wav' in file:
                os.remove('clips_library/' + file)
