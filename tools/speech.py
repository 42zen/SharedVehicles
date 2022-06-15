from playsound import playsound
from gtts import gTTS

def google(text, lang='en'):
    myobj = gTTS(text=text, lang=lang, slow=False)
    myobj.save('speech.mp3')
    playsound('speech.mp3')

def say(text, lang='en', src='google'):
    return google(text, lang=lang)
