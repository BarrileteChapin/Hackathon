import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import numpy as np

def record_and_transcribe(filename="input.wav",data=[], sample_rate=16000):
    """Records audio from the microphone and transcribes it to text.

    Args:
        filename (str, optional): The filename to save the audio. Defaults to "output.wav".
        duration (int, optional): The recording duration in seconds. Defaults to 5.
        sample_rate (int, optional): The sample rate for the recording. Defaults to 44100.
    
    Returns:
        str: The transcribed text, or None if an error occurred.
    """
    try:
        recording = np.concatenate(data, axis=0)
        sf.write(filename, recording, sample_rate)

        r = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from speech recognition service; {e}"
    except Exception as e:
        return f"An error occurred during recording/transcription: {e}"
