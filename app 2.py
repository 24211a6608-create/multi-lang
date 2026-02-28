import streamlit as st
from subtitle_pipeline import SubtitleMLPipeline
from pathlib import Path
import subprocess

st.set_page_config(page_title="SubtiAI", layout="wide")
st.title("🌍 SubtiAI – Global Subtitle Generator")

pipeline = SubtitleMLPipeline()

languages = pipeline.supported_languages

output_lang = st.selectbox("Translate To (Optional)", ["None"] + languages)

tab1, tab2, tab3 = st.tabs(["🎞 Video", "🎧 Audio", "📝 Text"])

# VIDEO
with tab1:
    video = st.file_uploader("Upload video", type=["mp4","mov","avi"])
    if video:
        Path("temp_video.mp4").write_bytes(video.read())

        if st.button("Generate Video Subtitles"):
            subprocess.run(["ffmpeg","-y","-i","temp_video.mp4","temp_audio.wav"])

            out="video.srt"
            tgt = None if output_lang=="None" else output_lang

            pipeline.audio_to_srt("temp_audio.wav", out, tgt)

            srt=open(out, encoding="utf-8").read()
            st.text_area("Subtitles", srt, height=300)
            st.download_button("Download SRT", srt, "video_subtitles.srt")

# AUDIO
with tab2:
    audio = st.file_uploader("Upload audio", type=["wav","mp3"])
    if audio:
        Path("temp_audio.wav").write_bytes(audio.read())

        if st.button("Generate Audio Subtitles"):
            out="audio.srt"
            tgt = None if output_lang=="None" else output_lang

            pipeline.audio_to_srt("temp_audio.wav", out, tgt)

            srt=open(out, encoding="utf-8").read()
            st.text_area("Subtitles", srt, height=300)
            st.download_button("Download SRT", srt, "audio_subtitles.srt")

# TEXT
with tab3:
    text = st.text_area("Enter text")
    if st.button("Generate Text Subtitles"):
        out="text.srt"
        pipeline.text_to_srt(text, out)

        srt=open(out, encoding="utf-8").read()
        st.text_area("Subtitles", srt, height=300)
        st.download_button("Download SRT", srt, "text_subtitles.srt")