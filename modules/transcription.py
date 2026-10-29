import whisper

model = whisper.load_model("base")

def transcribe_audio(audio_path):
    try:
        result = model.transcribe(audio_path,
                                  fp16=False)
        print(result["text"])   # Debug

        return result["text"]

    except Exception as e:
       import streamlit as st
       print("Whisper error:",e)
       st.error(f"Whisper Error: {e}")
    
   