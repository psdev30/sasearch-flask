from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment
import speech_recognition as sr
import os


class Conversions:

    def caw():
        clipDirectory = 'C:/Users/psjuk/SASearch/clips_library/'
        # for filename in os.listdir(clipDirectory):
        #     os.system("ffmpeg -i {0} -acodec pcm_s16le -ar 16000 out.wav".format(filename))

    def convertToMp3(fileName):
        mp4 = 'clips_library/' + fileName + '.mp4'
        mp3 = fileName + '.mp3'
        wav = fileName + '.wav'
        videoClip = VideoFileClip(mp4)
        audioClip = videoClip.audio
        audioClip.write_audiofile(mp3)
        audioClip.close()
        videoClip.close()
        return wav, mp3

    def convertToWav(wav, mp3):
        filepath = os.path.abspath(mp3)
        sound = AudioSegment.from_mp3(filepath).export(wav, format="wav")

    def extract_text(wav, fileName):
        r = sr.Recognizer()
        with sr.WavFile(os.path.abspath(wav)) as source:
            audio = r.record(source)
            text = r.recognize_google(audio)
            name = fileName.title()
            if '_' in fileName:
                name = name.replace('_', ' ')
            short_path = fileName + '.mp4'
        os.remove(fileName + '.mp3')
        os.remove(fileName + '.wav')
        return name, short_path, text
