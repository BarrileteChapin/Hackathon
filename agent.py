import google.generativeai as genai
import os
import base64
import re

class Agent: 
    def __init__(self): 
        # Configure the Gemini API
        os.environ["GOOGLE_API_KEY"] = "AIzaSyB2haGEeWLiv1cDWMMw_MpBFFU0ThTcNAo" 
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

        # Select the Gemini model (e.g., "gemini-pro")
        self.model = genai.GenerativeModel('gemini-1.5-flash')

        # Regular expression for matching social media URLs (improve as needed)
        self.social_media_regex = r"(facebook\.com|twitter\.com|instagram\.com|youtube\.com|tiktok\.com|linkedin\.com)"


    
    #image/text input
    def generate_gemini_response(self,image_path, prompt):
        try:
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

            image_data = {
                "mime_type": "image/jpeg",  # Adjust if your image is a different format
                "data": encoded_image
            }

            contents = [
                {
                    "parts": [  # Use "parts" for multimodal
                        {
                            "inline_data": {  # Use "inline_data" for images
                                "mime_type": "image/jpeg",
                                "data": encoded_image
                            }
                        },
                        {"text": prompt}
                    ]
                }
            ]

            response = self.model.generate_content(contents)
            return response.text

        except FileNotFoundError:
            return "Error: Image not found."
        except Exception as e:
            return f"An error occurred: {e}"

    def analyze_image_distractions(self,image_path):
        prompt = "Analyze this image. Does it contain elements suggesting a social media website (e.g., logos, interfaces, URLs)? Answer with 'yes' or 'no'."
        gemini_response = self.generate_gemini_response(image_path, prompt)
        if gemini_response:
            match = re.search(self.social_media_regex, gemini_response.lower())
            if match:
                return "Distraction_detected: yes"
            elif "yes" in gemini_response.lower():
                return "Distraction_detected: yes"
            else:
                return "Distraction_detected: no"
        else:
            return "Distraction_detected: Unknown"

    def is_person_happy(self,image_path):
        prompt = "Is the person in this image happy? Answer with one of these options: Happy, Sad, Anxious, Neutral. And explain briefly."
        gemini_response = self.generate_gemini_response(image_path, prompt)
        if gemini_response:
            emotion_match = re.search(r"(Happy|Sad|Anxious|Neutral)", gemini_response, re.IGNORECASE)
            if emotion_match:
                emotion = emotion_match.group(1)
                if emotion.lower() not in ("happy", "neutral"):
                    motivational_message = "Remember, it's okay not to be okay. Take a deep breath and focus on what you can control."
                    return f"Emotion: {emotion}\nMotivational message: {motivational_message}"
                else:
                    return f"Emotion: {emotion}"
            else:
                return "Emotion: Unknown"
        else:
            return "Emotion: Unknown"

    def act_as_therapist(self,text_input):
        prompt = f"Act as a therapist and respond to the following: {text_input}"
        response = self.model.generate_content(prompt) # Text only
        return response.text



