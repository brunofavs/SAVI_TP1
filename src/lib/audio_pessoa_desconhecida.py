#!/usr/bin/env python3
from gtts import gTTS
import tkinter as tk
from functools import partial
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame   

# mytext = "Hello, I don't know you. Please tell me your name." 
# language = 'en'

# myobj = gTTS(text=mytext, lang=language, slow=False)
# myobj.save("Welcome.mp3")

# pygame.init()
# pygame.mixer.music.load("Welcome.mp3")
# pygame.mixer.music.play()
# while pygame.mixer.music.get_busy():
#     pygame.time.Clock().tick(10)

def play_welcome():
    mytext = "Hello, I don't know you. Please tell me your name."
    language = 'en'

    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("Welcome.mp3")

    pygame.init()
    pygame.mixer.music.load("Welcome.mp3")
    pygame.mixer.music.play()
    
    # while pygame.mixer.music.get_busy():
    #     pygame.time.Clock().tick(10)

def play_name(event=None,entry = None,root = None,name_var = None):

    name = entry.get()
    name_var.set(name)
    language = 'en'

    if name:

        mytext2 = f'Thank you {name}, for providing your name'
        myobj2 = gTTS(text=mytext2, lang=language, slow=False)
        myobj2.save("Thank_you.mp3")

        pygame.mixer.music.load("Thank_you.mp3")
        pygame.mixer.music.play()
    root.destroy()
        

def name_prompt():

    root = tk.Tk()
    root.title("User Details")

    label = tk.Label(root, text="Please enter your name:")
    label.pack()
    
    name_var = tk.StringVar()

    entry = tk.Entry(root)
    entry.pack()
    entry.bind("<Return>", partial(play_name,entry = entry,root = root,name_var = name_var))  # Chama save_name ao pressionar Enter

    button_save = tk.Button(root, text="Save Name", command=partial(play_name,entry = entry,root = root,name_var = name_var))
    button_save.pack()

    # root.update()
    # root.update_idletasks()
    root.mainloop()

    return name_var.get()
        