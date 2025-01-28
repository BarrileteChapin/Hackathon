import tkinter as tk
from tkinter import ttk
from gtts import gTTS
import pygame
import threading
from PIL import Image, ImageTk, ImageSequence
import os

class Buddy:
    def __init__(self, master): #take the main window as parameter
        self.master = master
        self.image_label = ttk.Label(master)
        self.image_label.pack()
        self.transcript_label = ttk.Label(master, wraplength=350)
        self.transcript_label.pack(pady=10)


    def play_audio_with_gif_gui(self, text, image_path="robot_talking.gif", audio_file="tts.mp3"):
        try:
            img = Image.open(image_path)
            if img.format == "GIF":
                self.frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(img)]
            else:
                self.frames = [ImageTk.PhotoImage(img)]

            self.animate_gif() #call the animate gif function

        except FileNotFoundError:
            error_label = ttk.Label(self.master, text=f"Error: Image file not found at {image_path}")
            error_label.pack()
            return

        self.transcript_label.config(text=text) #set the text

        def play_audio():
            pygame.mixer.init()
            try:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                audio_path = os.path.join(script_dir, audio_file)
                tts = gTTS(text=text, lang="en")
                tts.save(audio_path)
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            except pygame.error as e:
                print(f"Error playing audio with pygame: {e}")
            finally:
                pygame.mixer.quit()
                self.master.after(0, self.master.destroy) # close the main window

        audio_thread = threading.Thread(target=play_audio)
        audio_thread.start()

    def animate_gif(self, frame_index=0):
        self.image_label.config(image=self.frames[frame_index])
        self.master.after(50, self.animate_gif, (frame_index + 1) % len(self.frames))
