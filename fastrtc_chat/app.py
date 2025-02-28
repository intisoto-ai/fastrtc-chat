import fastrtc
import gradio as gr
from fastrtc_chat.speech import process_audio

# Define the chat processing function
def real_time_chat(audio):
    return process_audio(audio)

# Launch the application
if __name__ == "__main__":
    fastrtc.launch(real_time_chat)
