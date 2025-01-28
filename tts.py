import pygame
import os
from PIL import Image, ImageSequence
import threading
from gtts import gTTS
import time

class Buddy:
    def __init__(self, screen):
        self.screen = screen
        self.frames = []
        self.current_frame = 0
        self.image_rect = None
        self.font = pygame.font.Font(None, 30)
        self.text = ""

    def play_audio_with_gif_gui(self, text, image_path="robot_talking.gif", audio_file="tts.mp3"):
        try:
            img = Image.open(image_path)
            if img.format == "GIF":
                self.frames = [pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode).convert_alpha() for frame in ImageSequence.Iterator(img)]
                self.image_rect = self.frames[0].get_rect()
                self.image_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
            else:
                self.frames = [pygame.image.load(image_path).convert_alpha()]
                self.image_rect = self.frames[0].get_rect()
                self.image_rect.center = (self.screen.get_width() // 2, self.creen.get_height() // 2)

            self.text = text

            def play_audio(text):
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

            pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)

            audio_thread = threading.Thread(target=play_audio, args=(text,), daemon=True)
            audio_thread.start()

        except FileNotFoundError:
            print(f"Error: Image file not found at {image_path}")
            return

    def draw(self):
        if self.frames:
            self.screen.blit(self.frames[self.current_frame], self.image_rect)
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (self.screen.get_width() // 2, self.screen.get_height() - 50)
        self.screen.blit(text_surface, text_rect)



class PygameManager:  # New class for calling the tts easily
    def __init__(self):
        self.screen = None
        self.buddy = None
        self.running = False
        self.clock = None

    def run_loop(self, text_to_display):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption("Buddy with Pygame")
        self.buddy = Buddy(self.screen)

        def audio_finished():
            self.running = False

        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)

        self.running = True
        self.clock = pygame.time.Clock()

        self.buddy.play_audio_with_gif_gui(text_to_display)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.USEREVENT + 1:
                    audio_finished()

            self.screen.fill((0, 0, 0))
            self.buddy.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

''''
def talkTTS(text):
    pygame_manager = PygameManager()  # Create an instance
    pygame_manager.run_loop(text)

text_to_display = "This is a test!"
talkTTS(text_to_display)
'''