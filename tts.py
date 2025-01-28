import tkinter as tk
from tkinter import ttk
from gtts import gTTS
import pygame
import threading
from PIL import Image, ImageTk, ImageSequence
import os

class Buddy:
    def __init__(self, master):
        self.master = master
        self.image_label = ttk.Label(master)
        self.image_label.pack()
        self.transcript_label = ttk.Label(master, wraplength=350)
        self.transcript_label.pack(pady=10)
        self.frames = []
        self._animation_id = None  # Track animation frame updates

    def play_audio_with_gif_gui(self, text, image_path="robot_talking.gif", audio_file="tts.mp3"):
        # Cancel any existing animation first
        if self._animation_id:
            self.master.after_cancel(self._animation_id)
            self._animation_id = None

        if not hasattr(ImageSequence, 'Iterator') or not Image.open(image_path).is_animated:
            self.frames = [ImageTk.PhotoImage(Image.open(image_path))]
        # Keep persistent reference to frames
        self.frames = [ImageTk.PhotoImage(frame.copy()) 
                    for frame in ImageSequence.Iterator(Image.open(image_path))]
        
        # Start animation in main thread
        self.master.after(0, self._start_animation_and_audio, text, audio_file)

    def animate_gif(self, frame_index=0):
        if self.frames:
            try:
                self.image_label.config(image=self.frames[frame_index])
            except tk.TclError:
                return  # Prevent crash if window closed
            self._animation_id = self.master.after(50, self.animate_gif, 
                                                (frame_index + 1) % len(self.frames))

    def _start_animation_and_audio(self, text, audio_file):
        if not self.master.winfo_exists():
            return  # Prevent call on destroyed window
        self.animate_gif()
        self.transcript_label.config(text=text)
        threading.Thread(target=self._play_audio, args=(text, audio_file), daemon=True).start()

    def _play_audio(self, text, audio_file):
        # Existing audio code with error handling
        try:
            tts = gTTS(text=text, lang="en")
            tts.save(audio_file)
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            self.master.after(0, self._show_error, f"Audio Error: {str(e)}")
        finally:
            pygame.mixer.quit()

    def _show_error(self, message):
        self.transcript_label.config(text=message, foreground="red")




