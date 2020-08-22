import time

from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment
import speech_recognition as sr
import os
import cloudinary, cloudinary.uploader, cloudinary.api


class Conversions:

    def convert_to_mp3(file_name):
        mp4 = 'clips_library/' + file_name + '.mp4'
        mp3 = 'clips_library/' + file_name + '.mp3'
        wav = 'clips_library/' + file_name + '.wav'
        video_clip = VideoFileClip(mp4)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(mp3)
        audio_clip.close()
        video_clip.close()

        return wav, mp3

    def convert_to_wav(wav, mp3):
        sound = AudioSegment.from_mp3(mp3)
        sound.export(wav, format="wav")
        return

    def extract_text(wav, file_name):
        r = sr.Recognizer()
        with sr.WavFile(os.path.abspath(wav)) as source:
            try:
                audio = r.record(source)
                text = r.recognize_google(audio)
                name = file_name.title()
                if '_' in file_name:
                    name = name.replace('_', ' ')
                short_path = file_name + '.mp4'
                os.remove('clips_library/' + file_name + '.mp3')
                os.remove('clips_library/' + file_name + '.wav')
                return name, short_path, text

            except:
                os.remove('clips_library/' + file_name + '.mp4')
                os.remove('clips_library/' + file_name + '.mp3')
                os.remove('clips_library/' + file_name + '.wav')
                return 'clip audio is unreadable'
