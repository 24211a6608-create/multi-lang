import streamlit as st
from subtitle_pipeline import SubtitleMLPipeline
from pathlib import Path
import tempfile
import subprocess

st.set_page_config(page_title="Subti 🌍",layout="wide")
st.markdown("""
<style>
.main-title{font-size:40px;font-weight:800;color:#4a90e2}
.subtitle{color:#666;margin-bottom:20px}
.box{background:#f7f9fc;padding:20px;border-radius:12px}
</style>
""",unsafe_allow_html=True)

st.markdown('<div class="main-title">🌍 Subti</div>',unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI Subtitle Generator with Translation</div>',unsafe_allow_html=True)

@st.cache_resource
def load():
    return SubtitleMLPipeline()

pipeline=load()

# ───── Sidebar ─────
with st.sidebar:
    st.header("⚙️ Settings")

    target_lang=st.selectbox(
        "Translate subtitles to",
        ["No Translation","English","Hindi","Bengali","Tamil","Telugu","Marathi","Urdu"]
    )

    tgt=None if target_lang=="No Translation" else target_lang

# ───── Tabs ─────
tab1,tab2,tab3=st.tabs(["🎞 Video","🎧 Audio","📝 Text"])

def show(srt):
    st.text_area("Output",srt,height=300)
    st.download_button("Download SRT",srt,"subtitles.srt")

# VIDEO
with tab1:
    file=st.file_uploader("Upload video",type=["mp4","mov","avi","mkv"])
    if file and st.button("Generate Video Subtitles"):
        v=tempfile.NamedTemporaryFile(delete=False,suffix=".mp4")
        v.write(file.read())

        a=tempfile.NamedTemporaryFile(delete=False,suffix=".wav")

        subprocess.run(["ffmpeg","-y","-i",v.name,"-ar","16000","-ac","1",a.name])

        out=tempfile.NamedTemporaryFile(delete=False,suffix=".srt").name
        pipeline.audio_to_srt(a.name,out,target_lang=tgt)
        show(Path(out).read_text())

# AUDIO
with tab2:
    file=st.file_uploader("Upload audio",type=["wav","mp3","m4a"])
    if file and st.button("Generate Audio Subtitles"):
        a=tempfile.NamedTemporaryFile(delete=False)
        a.write(file.read())

        out=tempfile.NamedTemporaryFile(delete=False,suffix=".srt").name
        pipeline.audio_to_srt(a.name,out,target_lang=tgt)
        show(Path(out).read_text())

# TEXT
with tab3:
    text=st.text_area("Enter text")
    if text and st.button("Generate Text Subtitles"):
        out=tempfile.NamedTemporaryFile(delete=False,suffix=".srt").name
        pipeline.text_to_srt(text,out,target_lang=tgt)
        show(Path(out).read_text())