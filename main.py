from monitoring import *
from tts import *
from agent import * 
from TherapyGui import *
import tkinter as tk
from tkinter import ttk, messagebox
from report import SimpleReportApp
import datetime

#styling (GUI)
#BACKGROUND_COLOR = "#f0f0f0"  # Example background color
#BUTTON_COLOR = "#4CAF50"  # Example button color
#FONT = ("Arial", 20)  # Example font

#Agent instance
miniGemini = Agent()
#global flag to intervene while there is no break
distractionAllowed = False

#global vars for report
start_time = datetime.datetime.now()
count_distractions=10
count_badMood = 2

def generateReport():
    appReport = SimpleReportApp()
    temp_text= miniGemini.generate_gemini_report(start_time, count_distractions,count_badMood)
    print(f'text from report is: {temp_text} ')
    appReport.start(temp_text[0],temp_text[1])

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
        
        tempDistraction = results.get("distraction")
        tempHappiness = results.get("happiness")
        
        print(tempDistraction)
        print(tempHappiness)

        if("yes" in tempHappiness):
            count_badMood+=1
        if ("yes" in tempDistraction): 
            count_distractions+=1    
            if("yes" in tempHappiness):
                #we need to intervene
                tempBuddy = PygameManager()
                tempBuddy.run_loop("Remember, I am here for supporting you!", "ca") #we can ask the agent to improvise something as well
            

        #delay
        time.sleep(30)


def therapy(text_input):
    therapist = miniGemini.act_as_therapist(text_input)
    print(therapist)


def open_therapy_gui():
    global therapy_window # Declare therapy_window as global
    if therapy_window is None or not tk.Toplevel.winfo_exists(therapy_window):
        therapy_window = tk.Toplevel(root)
        therapy_gui = TherapyGUI(therapy_window, miniGemini.act_as_therapist)
        therapy_window.lift()
        therapy_window.focus_force()
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

        report_button_therapy = ttk.Button(therapy_window, text="Report", command=generateReport)
        report_button_therapy.pack(pady=10)

        therapy_window.protocol("WM_DELETE_WINDOW", lambda: on_closing_therapy(therapy_window))



def on_closing(master):
    global running_periodic
    print("closes?")
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        master.destroy()
        running_periodic = False

def on_closing_therapy(window):
    print("close_therapy? ")
    window.destroy()
    on_closing(root)
    #generateReport()

def mainGUI():
    global root, therapy_window,running_periodic
    root = tk.Tk()  # Only ONE Tk instance
    root.title("Study Buddy - Main Menu")
    root.configure(bg=BACKGROUND_COLOR)
    therapy_window = None
    running_periodic = False

    # Center the window (styling):
    #style = ttk.Style()
    #print(style.theme_names())  # Print available themes
    #style.theme_use("xpnative")
    window_width = 300  # Adjust as needed
    window_height = 200  # Adjust as needed
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def start_app():
        root.withdraw()
        #root.iconify()
        open_therapy_gui()

    def close_app():
        print("close last")
        on_closing(root)

    # Style configuration
    #style.configure("Start.TButton", font=FONT, background=BUTTON_COLOR, foreground="white")  # Green button
    #style.configure("Close.TButton", font=FONT, background="red", foreground="white") # Red button

    
    start_button = ttk.Button(root, text="Start", command=start_app, style="Start.TButton")
    start_button.pack(pady=20)

    close_button = ttk.Button(root, text="Close", command=close_app, style="Close.TButton")
    close_button.pack(pady=10)

    
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    root.mainloop()

global running_periodic
running_periodic = False


if __name__ == "__main__":
    mainGUI()



