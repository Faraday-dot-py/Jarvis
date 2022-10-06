import pygame
from gtts import gTTS

pygame.mixer.init(27100)
#pygame.mixer.init()

language = 'en'
topLevelDomain = 'co.za'

def say(sentence):
    #Converts the given string into an audio file
    words = gTTS(text=sentence, lang=language, tld=topLevelDomain, slow=False)

    #Saves the outputted audio file to be played back later as an mp3
    words.save("speech.mp3")
    
    #Loads sound into pygame mixer
    pygame.mixer.music.load("speech.mp3")
    
    #Plays generated audio
    pygame.mixer.music.play()
    
#en-US-Standard-I
    
def stopSpeaking(noise):
    noise.stop()

