from monitoring import *
from tts import *



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