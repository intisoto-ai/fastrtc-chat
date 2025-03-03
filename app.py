# app.py
import logging
import gradio as gr
from fastrtc import Stream, ReplyOnPause
from fastrtc_chat.speech import process_audio
# import uvicorn  # Removed uvicorn import

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

def app_process_audio(audio):
    for item in process_audio(audio):
        if item is not None:
          if isinstance(item, tuple) and len(item) == 2:
            sample_rate, audio_chunk = item
            yield sample_rate, audio_chunk
          else:
            log.error(f"Process audio return an element that is not a tuple of len 2 but : {item}")
        else:
            yield None

stream = Stream(ReplyOnPause(app_process_audio), modality="audio", mode="send-receive")

if __name__ == "__main__":
    ui = stream.ui  # Now we have a ui object, we are not launching it
    # uvicorn.run(ui, host="0.0.0.0", port=7860, reload=True) #Removed uvicorn line
    ui.launch(server_name="0.0.0.0", server_port=7860,show_api=False) # Launch directly with gradio
