# fastrtc_chat/app.py
import logging
from fastrtc import Stream, ReplyOnPause
from fastrtc_chat.speech import process_audio

log = logging.getLogger(__name__)
# Configure logging
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

# Create the stream and launch
stream = Stream(ReplyOnPause(process_audio), modality="audio", mode="send-receive")
stream.ui.launch()
