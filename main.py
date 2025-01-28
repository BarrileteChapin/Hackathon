from monitoring import *
from tts import *
from agent import * 
from TherapyGui import *
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

#Agent instance
miniGemini = Agent()
#global flag to intervene while there is no break
distractionAllowed = False



def checkDistraction():
    photo_path = "photo.jpg"
    screen_path = "screenshot.png"
    global running_periodic
    while running_periodic:
        results = {}
        def run_and_store(func, *args, key):
            results[key] = func(*args)
        
        #take photo + screenshot
        Monitoring.take_photo(photo_path)
        Monitoring.take_screenshot(screen_path)
        #send to Gemini for further analysis
        thread1 = threading.Thread(target=run_and_store, args=(miniGemini.analyze_image_distractions, screen_path), kwargs={"key": "distraction"})
        thread2 = threading.Thread(target=run_and_store, args=(miniGemini.is_person_happy, photo_path), kwargs={"key": "happiness"})

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()
        print(results.get("distraction"))
        print(results.get("happiness"))



        #delay
        time.sleep(30)


def therapy(text_input):
    therapist = miniGemini.act_as_therapist(text_input)
    print(therapist)


def open_therapy_gui():
    global therapy_window  # Declare therapy_window as global
    if therapy_window is None or not tk.Toplevel.winfo_exists(therapy_window): #Check if window exists
        therapy_window = tk.Toplevel(root)
        therapy_gui = TherapyGUI(therapy_window, miniGemini.act_as_therapist)
        output_text = therapy_gui.output_text
        def start_tasks():
            global running_periodic
            if not running_periodic:
                running_periodic = True
                periodic_thread = threading.Thread(target=checkDistraction, daemon=True)
                periodic_thread.start()
                start_button_therapy.config(state=tk.DISABLED)
                stop_button_therapy.config(state=tk.NORMAL)

        def stop_tasks():
            global running_periodic
            if running_periodic:
                running_periodic = False
                start_button_therapy.config(state=tk.NORMAL)
                stop_button_therapy.config(state=tk.DISABLED)
                output_text.config(state=tk.NORMAL)
                output_text.insert(tk.END, "Periodic tasks stopped.\n")
                output_text.config(state=tk.DISABLED)

        start_button_therapy = ttk.Button(therapy_window, text="Start Periodic Tasks", command=start_tasks)
        start_button_therapy.pack(pady=10)

        stop_button_therapy = ttk.Button(therapy_window, text="Stop Periodic Tasks", command=stop_tasks, state=tk.DISABLED)
        stop_button_therapy.pack(pady=10)
        therapy_window.protocol("WM_DELETE_WINDOW", lambda: on_closing_therapy(therapy_window))



def on_closing(master):
    global running_periodic
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        master.destroy()
        running_periodic = False

def on_closing_therapy(window):
    window.destroy()

def mainGUI():
    global root, therapy_window, running_periodic
    root = tk.Tk()  # Only ONE Tk instance
    root.title("Gemini App - Main Menu")
    root.configure(bg=BACKGROUND_COLOR)
    therapy_window = None
    running_periodic = False

    def start_app():
        root.withdraw()  # Hide the menu window
        open_therapy_gui()

    def close_app():
        on_closing(root)

    start_button = ttk.Button(root, text="Start", command=start_app)
    start_button.pack(pady=20)

    close_button = ttk.Button(root, text="Close", command=close_app)
    close_button.pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    root.mainloop()

    

if __name__ == "__main__":
    mainGUI()


'''
if __name__ == "__main__":
    #run distraction check... it exits when program is terminated
    periodic_thread = threading.Thread(target=checkDistraction, daemon=True) 
    periodic_thread.start()
    # Example usage: tts
    text = "Hello, Trainer! I've been waiting for you."
    image_path = "robot_talking.gif"
    audio_file = "output.mp3"
    Buddy.play_audio_with_gif_gui(text,image_path,audio_file) 
    
    while True:
        text_input = input("Enter text for therapy (or type 'exit'): ")
        if text_input.lower() == "exit":
            programRunning=False
            break
        therapy_thread = threading.Thread(target=therapy, args=(text_input,))
        therapy_thread.start()
'''