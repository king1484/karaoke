from audio_separator import Separator
import subprocess
import os
import uuid
import streamlit as st
from pydub import AudioSegment

st.title("Karaoke")
url = st.text_area("Enter spotify song URL")
button = st.button("Process")

if button:
    with st.spinner("Processing"):
        uuid_str = str(uuid.uuid4())
        cmd = f"spotdl {url} --output audio{uuid_str}"
        subprocess.run(cmd, shell=True)
        files = os.listdir(f"audio{uuid_str}")
        audio_files = [file for file in files if file.endswith(('.mp3', '.wav', '.ogg'))]
        old_path = os.path.join(f"audio{uuid_str}", audio_files[0])
        new_path = os.path.join(f"audio{uuid_str}", "audio.mp3")
        os.rename(old_path, new_path)
    
        separator = Separator(f'audio{uuid_str}/audio.mp3', model_name='UVR-MDX-NET-Inst_HQ_3', 
                              use_cuda=True, primary_stem_path=f"music{uuid_str}.wav", output_single_stem="instrumental")
        primary_stem_path = separator.separate()
        
        sound = AudioSegment.from_wav(f"music{uuid_str}.wav")
        sound.export("output.mp3", format="mp3", bitrate="192k")
    
        os.remove(f"music{uuid_str}.wav")
        os.remove(f"audio{uuid_str}/audio.mp3")
        os.rmdir(f"audio{uuid_str}")
    
        st.audio("output.mp3", format="audio/mp3")
