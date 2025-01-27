import google.generativeai as genai
import os
import base64

# Configure the Gemini API
os.environ["GOOGLE_API_KEY"] = "AIzaSyB2haGEeWLiv1cDWMMw_MpBFFU0ThTcNAo" 
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Select the Gemini model (e.g., "gemini-pro")
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_gemini_response(image_path, prompt):
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

        response = model.generate_content(contents)
        return response.text

    except FileNotFoundError:
        return "Error: Image not found."
    except Exception as e:
        return f"An error occurred: {e}"


# Example usage:
image_path = "robot.png"  # Replace with the path to your image
prompt = "Describe the emotions on this image. Is it happy/sad/frustaded/neutral?"
response_text = generate_gemini_response(image_path, prompt)

if response_text:
    print(response_text)