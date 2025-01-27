#monitoring part
import pyautogui
import time
import cv2

class Monitoring: 

    def take_screenshot(filename="screenshot.png"):
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            print(f"Screenshot saved as {filename}")
        except Exception as e:
            print(f"Error taking screenshot: {e}")


    def take_photo(filename="photo.jpg"):
        try:
            # Open the default camera
            video_capture = cv2.VideoCapture(0)

            if not video_capture.isOpened():
                raise IOError("Cannot open webcam")

            # Read a frame
            ret, frame = video_capture.read()

            if ret:
                # Save the frame
                cv2.imwrite(filename, frame)
                print(f"Photo saved as {filename}")
            else:
                print("Could not capture frame.")

            # Release the camera
            video_capture.release()
        except IOError as e:
            print(f"IOError: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


