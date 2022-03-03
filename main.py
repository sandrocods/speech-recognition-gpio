from pydub import AudioSegment
import telebot
import RPi.GPIO as GPIO
import speech_recognition as sr

bot = telebot.TeleBot("5223878902:AAEr-lqu6TnH9AQRDCb5htnDpN11kojEs9E", parse_mode=None)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)


@bot.message_handler(content_types=['audio', 'voice'])
def handle_docs_audio(message):
    print(f"New Audio Receive", end="\n")

    if message.content_type == "audio":
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    else:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

    with open("audio.mp3", "wb") as new_file:
        new_file.write(downloaded_file)

    AudioSegment.from_file("audio.mp3").export("audio.wav", format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile("audio.wav") as source:
        audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio, language="id")
        print(f"Recognize Text : " + text, end="\n")

    if text.lower() == "turn on the lamp":
        bot.reply_to(message, "Lamp ON 😁")
        GPIO.output(27, True)
        print(f"~ Lamp ON", end="\n")

    elif text.lower() == "turn off the lamp":
        bot.reply_to(message, "Lamp Off 😁")
        GPIO.output(27, False)
        print(f"~ Lamp Off", end="\n")

    else:
        print(f"~ Sorry i dont know ", end="\n")
        bot.reply_to(message, "Sorry i dont know 😢")



bot.polling()