#!/usr/bin/env python3
from gtts import gTTS
import pygame
import tkinter as tk

mytext = "Hello, I don't know you. Please tell me your name." 
language = 'en'

myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("Welcome.mp3")

pygame.init()
pygame.mixer.music.load("Welcome.mp3")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

def play_welcome():
    mytext = "Hello, I don't know you. Please tell me your name."
    language = 'en'

    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("Welcome.mp3")

    pygame.init()
    pygame.mixer.music.load("Welcome.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def save_name(event=None):
    name = entry.get()
    if name:
        filename = f"{name}.txt"
        with open(filename, 'w') as file:
            file.write(f"User Name: {name}\n")

        mytext2 = f'Thank you {name}, for providing your name'
        myobj2 = gTTS(text=mytext2, lang=language, slow=False)
        myobj2.save("Thank_you.mp3")

        pygame.mixer.music.load("Thank_you.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        print(f"File '{filename}' created with user name: {name}")
        root.destroy()

root = tk.Tk()
root.title("User Details")

label = tk.Label(root, text="Please enter your name:")
label.pack()

entry = tk.Entry(root)
entry.pack()
entry.bind("<Return>", save_name)  # Chama save_name ao pressionar Enter

button_save = tk.Button(root, text="Save Name", command=save_name)
button_save.pack()

root.mainloop()
