#!/usr/bin/env python3
from gtts import gTTS
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame   

def hello_again(name):

    mytext = f'Hello {name}'

    language = 'en'

    myobj = gTTS (text=mytext, lang = language , slow = False)
    myobj.save("Welcome_known.mp3")

    pygame.init()
    pygame.mixer.music.load("Welcome_known.mp3")
    pygame.mixer.music.play()

def goodbye(name):

    mytext = f'Goodbye {name}'

    language = 'en'

    myobj = gTTS (text=mytext, lang = language , slow = False)
    myobj.save("Goodbye.mp3")

    pygame.init()
    pygame.mixer.music.load("Goodbye.mp3")
    pygame.mixer.music.play()
