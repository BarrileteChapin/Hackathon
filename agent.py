import google.generativeai as genai
import os
import base64


class Agent: 
    def __init__(self): 
        # Configure the Gemini API
        os.environ["GOOGLE_API_KEY"] = "AIzaSyB2haGEeWLiv1cDWMMw_MpBFFU0ThTcNAo" 
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

        # Select the Gemini model (e.g., "gemini-pro")
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    
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

    def analyze_image_emotions(self,image_path):
        prompt = "Analyze the emotions expressed in this image."
        return self.generate_gemini_response(image_path, prompt)

    def is_person_happy(self,image_path):
        prompt = "Is the person in this image happy? Answer with yes or no and explain briefly."
        return self.generate_gemini_response(image_path, prompt)

    def act_as_therapist(self,text_input):
        prompt = f"Act as a therapist and respond to the following: {text_input}"
        response = self.model.generate_content(prompt) # Text only
        return response.text



# Example usage:
image_path1 = "robot.png"  # Replace with the path to your image
text_input="I have been feeling stressed" 

miniGemini = Agent()
emotion_analysis = miniGemini.analyze_image_emotions(image_path1)
happiness_check = miniGemini.is_person_happy(image_path1)
therapy_response = miniGemini.act_as_therapist(text_input)

print("Emotion Analysis:", emotion_analysis)
print("Happiness Check:", happiness_check)
print("Therapy Response:", therapy_response)  
 