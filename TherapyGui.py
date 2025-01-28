import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from transcription import *
from tts import Buddy

# Style configuration
BACKGROUND_COLOR = "#f0f0f0"  # Light gray background
BUTTON_COLOR = "#4CAF50"      # Green button
BUTTON_TEXT_COLOR = "white"
TEXT_COLOR = "#333333"      # Dark gray text
FONT_FAMILY = "Arial"        # Modern font
FONT_SIZE = 12

style = ttk.Style()
style.configure("TButton", background=BUTTON_COLOR, foreground=BUTTON_TEXT_COLOR, font=(FONT_FAMILY, FONT_SIZE))
style.configure("TLabel", background=BACKGROUND_COLOR, foreground=TEXT_COLOR, font=(FONT_FAMILY, FONT_SIZE))
style.configure("TFrame", background=BACKGROUND_COLOR)
style.configure("TEntry", font=(FONT_FAMILY, FONT_SIZE))
style.configure("TScrollbar", background=BACKGROUND_COLOR)

class TherapyGUI:
    def __init__(self, master, act_as_therapist_func,buddy):
        self.master = master
        self.master.title("Therapy Chat")
        self.master.configure(bg=BACKGROUND_COLOR)
        self.act_as_therapist = act_as_therapist_func
        self.buddy = buddy #Save the buddy object

        # Input Frame
        input_frame = ttk.Frame(self.master, padding=10)
        input_frame.pack(fill=tk.X)

        input_label = ttk.Label(input_frame, text="Your Input:")
        input_label.pack(anchor=tk.W)

        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=5, font=(FONT_FAMILY, FONT_SIZE))
        self.input_text.pack(fill=tk.X)

        # Buttons Frame
        button_frame = ttk.Frame(self.master, padding=10)
        button_frame.pack(fill=tk.X)

        self.record_button = ttk.Button(button_frame, text="Start Recording", command=self.start_recording)
        self.record_button.pack(side=tk.LEFT, padx=(0,5))
        self.stop_recording_button = ttk.Button(button_frame, text="Stop Recording", state=tk.DISABLED, command=self.stop_recording)
        self.stop_recording_button.pack(side=tk.LEFT, padx=(0,5))
        self.send_button = ttk.Button(button_frame, text="Send", command=self.send_text)
        self.send_button.pack(side=tk.LEFT, padx=(0,5))
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_text)
        self.clear_button.pack(side=tk.LEFT)

        # Output Frame
        output_frame = ttk.Frame(self.master, padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True)

        output_label = ttk.Label(output_frame, text="Therapy Response:")
        output_label.pack(anchor=tk.W)

        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, state=tk.DISABLED, font=(FONT_FAMILY, FONT_SIZE))
        self.output_text.pack(fill=tk.BOTH, expand=True)

        self.recording = False
        self.recorded_data = []
        self.recording_thread = None

    
    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.record_button.config(state=tk.DISABLED, text="Recording...")
            self.stop_recording_button.config(state=tk.NORMAL)
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, "Recording...\n")
            self.output_text.config(state=tk.DISABLED)
            self.recorded_frames = []

            def recording_thread_function():
                try:
                    fs = 44100
                    with sd.InputStream(samplerate=fs, channels=1) as stream:
                        while self.recording:
                            data, overflowed = stream.read(1024)
                            if data is not None:
                                self.recorded_frames.append(data)
                    if self.recorded_frames:
                        myrecording = np.concatenate(self.recorded_frames, axis=0)
                        sf.write("input.wav", myrecording, fs)
                        transcribed_text = record_and_transcribe(data = self.recorded_frames, sample_rate = fs) #Call with the data
                        if transcribed_text:
                            self.output_text.config(state=tk.NORMAL)
                            self.output_text.insert(tk.END, "You (Voice): " + transcribed_text + "\n")
                            self.output_text.config(state=tk.DISABLED)
                            self.master.after(0, self.send_text_from_voice, transcribed_text)
                    else:
                         self.output_text.config(state=tk.NORMAL)
                         self.output_text.insert(tk.END, "No audio recorded\n")
                         self.output_text.config(state=tk.DISABLED)
                except Exception as e:
                    print(f"Error during recording: {e}")
                    self.output_text.config(state=tk.NORMAL)
                    self.output_text.insert(tk.END, f"Error during recording: {e}\n")
                    self.output_text.config(state=tk.DISABLED)
                finally:
                    self.recording = False
                    self.recorded_frames = []
                    self.record_button.config(state=tk.NORMAL, text="Start Recording")
                    self.stop_recording_button.config(state=tk.DISABLED)

            self.recording_thread = threading.Thread(target=recording_thread_function)
            self.recording_thread.start()

    def stop_recording(self):
        self.recording = False

    def clear_text(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL) #Enable edition
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED) #Disable edition

    def process_recorded_audio(self, filename):
        try:
            r = sr.Recognizer()
            with sr.AudioFile(filename) as source:
                audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from speech recognition service; {e}"
        except Exception as e:
            return f"An error occurred during transcription: {e}"

    def send_text_from_voice(self, user_text):
        print("goes here -speech ")
        print(user_text)
        #if user_text:
        def run_therapy_task(text_input):
            therapy_response = self.act_as_therapist(text_input)
            self.output_text.config(state=tk.NORMAL)  # Enable edition
            self.output_text.insert(tk.END, therapy_response + "\n")
            self.output_text.config(state=tk.DISABLED)  # Disable edition
            #self.buddy.play_audio_with_gif_gui(therapy_response) #Call the buddy function

        therapy_thread = threading.Thread(target=run_therapy_task, args=(user_text,))
        therapy_thread.start()
        print("or maybe not")

    def send_text(self):
        user_text = self.input_text.get("1.0", tk.END).strip()
        if user_text:
            self.input_text.delete("1.0", tk.END)  # Clear the input text
            self.output_text.config(state=tk.NORMAL)  # Enable edition
            self.output_text.insert(tk.END, "You: " + user_text + "\n")
            self.output_text.config(state=tk.DISABLED)  # Disable edition

            def run_therapy_task(text_input):
                therapy_response = self.act_as_therapist(text_input)
                self.output_text.config(state=tk.NORMAL)  # Enable edition
                self.output_text.insert(tk.END, therapy_response + "\n")
                self.output_text.config(state=tk.DISABLED)  # Disable edition

            therapy_thread = threading.Thread(target=run_therapy_task, args=(user_text,))
            therapy_thread.start()

    def clear_text(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)  # Enable edition
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)  # Disable edition