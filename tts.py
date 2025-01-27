import tkinter as tk
from tkinter import ttk #GUI
from gtts import gTTS #the tts
import playsound #play audio
import threading #Threads 1. Audio 2. GUI (otherwise, when playing audio... everything freezes)
from PIL import Image, ImageTk, ImageSequence #handle images shown
import io #bits streaming from GIF 


class Buddy:
    
    def play_audio_with_gif_gui(text, image_path, audio_file):
        window = tk.Tk()
        window.title("Study Buddy")

        try:
            img = Image.open(image_path)
            if img.format == "GIF":
                frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(img)] #get a list of frames
            else:
                frames = [ImageTk.PhotoImage(img)] #otherwise only show one

            image_label = ttk.Label(window)
            image_label.pack()

            #magic occurs (display the gif animation)
            def animate_gif(frame_index=0):
                image_label.config(image=frames[frame_index])
                window.after(50, animate_gif, (frame_index + 1) % len(frames))
            
            animate_gif()

        except FileNotFoundError:
            error_label = ttk.Label(window, text=f"Error: Image file not found at {image_path}")
            error_label.pack()
            return

        transcript_label = ttk.Label(window, text=text, wraplength=350)
        transcript_label.pack(pady=10)

        def close_window():  # Function to close the window
            window.quit()
            window.destroy()

        def play_audio():
            playsound.playsound(audio_file)
            window.after(0, close_window) # Schedule the closing on the main thread

        audio_thread = threading.Thread(target=play_audio)
        audio_thread.start()

        window.mainloop()

        tts = gTTS(text=text, lang="en")
        tts.save(audio_file)    
        

