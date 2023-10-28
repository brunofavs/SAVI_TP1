#!/usr/bin/env python3
from gtts import gTTS
import pygame   
import os

file_path ='../imagens/alexandre.png'
file_name = os.path.basename(file_path)

file_name_no_extension = os.path.splitext(file_name)[0]

mytext = f'Hello {file_name_no_extension}'

language = 'en'

myobj = gTTS (text=mytext, lang = language , slow = False)
myobj.save("Welcome.mp3")

pygame.init()
pygame.mixer.music.load("Welcome.mp3")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
