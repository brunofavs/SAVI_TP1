#!/usr/bin/env python3
from gtts import gTTS
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame   

def temp():
    file_path ='../imagens/alexandre.png'
    file_name = os.path.basename(file_path)

    file_name_no_extension = os.path.splitext(file_name)[0]

    mytext = f'Hello {file_name_no_extension}'

    language = 'en'

    myobj = gTTS (text=mytext, lang = language , slow = False)
    myobj.save("Welcome_known.mp3")

    pygame.init()
    pygame.mixer.music.load("Welcome_known.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
