from audio_separator import Separator
import subprocess
import os
import uuid
import streamlit as st
from pydub import AudioSegment
from io import BytesIO

st.title("Karaoke")
uploaded_file = st.file_uploader("Upload an audio file (MP3, WAV, or OGG)", type=["mp3", "wav", "ogg"], key="file_uploader")
button = st.button("Process")

if button and uploaded_file:
    with st.spinner("Processing"):
        # Save the uploaded file
        audio_content = uploaded_file.read()
        uuid_str = str(uuid.uuid4())
        audio_path = f"audio{uuid_str}.mp3"  # Save as MP3 for compatibility
        with open(audio_path, "wb") as f:
            f.write(audio_content)

        separator = Separator(audio_path, model_name='UVR-MDX-NET-Inst_HQ_3', 
                                    primary_stem_path=f"music{uuid_str}.wav", output_single_stem="instrumental")
        primary_stem_path = separator.separate()
        
        sound = AudioSegment.from_wav(f"music{uuid_str}.wav")
        sound.export("output.mp3", format="mp3", bitrate="192k")
    
        os.remove(f"music{uuid_str}.wav")
        os.remove(audio_path)
    
        st.audio("output.mp3", format="audio/mp3")
        st.info("Processing complete. You can upload another file.")
