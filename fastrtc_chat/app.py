# fastrtc_chat/app.py
import logging
import gradio as gr
from fastrtc import Stream, ReplyOnPause
from fastrtc_chat.speech import process_audio
import uvicorn
import asyncio

log = logging.getLogger(__name__)
# Configure logging
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

async def app_process_audio(audio, state):
    """
    Process the audio and update the state with transcribed and translated text.
    """
    async for item in process_audio(audio):
        if item is not None:
            sample_rate, audio_chunk, transcribed_text, translated_text = item

            # Update state
            state["transcribed"] = transcribed_text
            state["translated"] = translated_text

            yield (sample_rate, audio_chunk), state
        else:
            yield None, state
        
    

# Create the stream and launch
stream = Stream(ReplyOnPause(app_process_audio), modality="audio", mode="send-receive")

if __name__ == "__main__":
    
    # UI definition
    with gr.Blocks() as ui:
        state = gr.State({"transcribed": "", "translated": ""})
        stream.ui()
        transcribed_textbox = gr.Textbox(label="Transcribed Text", interactive=False)
        translated_textbox = gr.Textbox(label="Translated Text", interactive=False)
        
        stream.ui.change(lambda x: [x["transcribed"], x["translated"]], [state], [transcribed_textbox, translated_textbox])

    ui.launch(prevent_thread_lock=True)
    uvicorn.run("fastrtc_chat.app:stream.ui.app", host="0.0.0.0", port=7860, reload=True)
