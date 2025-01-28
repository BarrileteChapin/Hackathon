import google.generativeai as genai
import os
import base64
import re
from tts import Buddy
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
        prompt = "Is the person in this image happy? Answer with one of these options: Happy, Sad, Anxious, Neutral"
        gemini_response = self.generate_gemini_response(image_path, prompt)
        if gemini_response:
            emotion_match = re.search(r"(Happy|Sad|Anxious|Neutral)", gemini_response, re.IGNORECASE)
            if emotion_match:
                if emotion_match.lower() not in ("happy", "neutral"):
                    return f"Intervention: yes\nEmotion: {emotion_match}"
                else:
                    return f"Intervention: no\nEmotion: {emotion_match}"
            else:
                return "Intervention: no\nEmotion: Unknown"
        else:
            return "Intervention: no\nEmotion: Unknown"

    def act_as_therapist(self,text_input):
        prompt = f'''Act as a therapist and study buddy in care of this person and respond to the following: {text_input} briefly (around 100-word limit) and offer help in any case.
        Please do not answer with asterisks or similar symbols'''

        response = self.model.generate_content(prompt) # Text only
        return response.text 

    def generate_gemini_report(self, start_time, count_distractions,count_badMood):
        #A report generated based on the time the conversation started
        
        try:
            prompt = f"""Generate a short report considering the conversation started at {start_time}.
            Every 30 seconds we count if there is a distraction or bad mood (anxious/sad). Here is our data
            No. Distractions: {count_distractions}, No. Bad mood: {count_badMood}.
            Repond positvely about the distractions detected in total, a score about stress levels, and focus
            in the following sample format:[Distractions=3, Stress=75%, Focus=30]
            Attach a short explanation as well (about 100 word-length)"""

            contents = [{"parts": [{"text": prompt}]}]  # Only text in the request

            response = self.model.generate_content(contents)
            #print(f'here-1 {response}')
            gemini_response_text = response.text
            #print(f'here-2 {gemini_response_text}')
            # Extract data using regex (handling potential variations)
            distractions_match = re.search(r"Distractions=(\d+)", gemini_response_text, re.IGNORECASE)
            stress_match = re.search(r"Stress=(\d+)%", gemini_response_text, re.IGNORECASE)
            focus_match = re.search(r"Focus=(\d+)", gemini_response_text, re.IGNORECASE)

            distractions = distractions_match.group(1) if distractions_match else "N/A"
            stress = stress_match.group(1) if stress_match else "N/A"
            focus = focus_match.group(1) if focus_match else "N/A"

            report_response = f"Distractions={distractions}, Stress={stress}%, Focus={focus}"
            return report_response, gemini_response_text

        except Exception as e:
            return f"An error occurred: {e}"

