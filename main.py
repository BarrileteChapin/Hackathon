from monitoring import *
from tts import *
from agent import * 

#Agent instance
miniGemini = Agent()

def run_tasks_in_threads():
    threads = []
    results = {}

    def run_and_store(func, *args, key):
        results[key] = func(*args)

    thread1 = threading.Thread(target=run_and_store, args=(miniGemini.analyze_image_emotions, image_a_path), kwargs={"key": "emotion"})
    thread2 = threading.Thread(target=run_and_store, args=(miniGemini.is_person_happy, image_b_path), kwargs={"key": "happiness"})
    thread3 = threading.Thread(target=run_and_store, args=(miniGemini.act_as_therapist, text_input), kwargs={"key": "therapy"})

    threads.extend([thread1, thread2, thread3])
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print("Emotion Analysis:", results["emotion"])
    print("Happiness Check:", results["happiness"])
    print("Therapy Response:", results["therapy"])

run_tasks_in_threads()


if __name__ == "__main__":
    # Example usage: tts
    text = "Hello, Trainer! I've been waiting for you."
    image_path = "robot_talking.gif"
    audio_file = "output.mp3"
    Buddy.play_audio_with_gif_gui(text,image_path,audio_file) 
    
    
    #monitoring part 
    Monitoring.take_photo()
    Monitoring.take_screenshot()
    time.sleep(5) #delay ... we can change it to 30s
    Monitoring.take_photo("photo2.jpg")
    Monitoring.take_screenshot("screenshot2.png")