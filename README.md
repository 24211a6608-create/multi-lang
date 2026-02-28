# 🎬 Subtitle ML Pipeline

A complete Python project for automatic subtitle generation and Whisper fine-tuning.

---

## Features

| Feature | Description |
|---|---|
| 🎥 Video → SRT | Extract audio from video and transcribe |
| 🎙️ Audio → SRT | Transcribe any audio file |
| 📝 Text → SRT | Convert plain text or JSON to timed subtitles |
| 🗂️ Dataset Builder | Slice audio by SRT timestamps for training |
| 🤖 Fine-Tuning | Fine-tune Whisper on your own data |

---

## Quick Start

```bash
pip install -r requirements.txt

# Video → SRT
python subtitle_pipeline.py video movie.mp4 output/subs.srt --model small

# Translate foreign video to English
python subtitle_pipeline.py video foreign.mp4 output/subs.srt --translate

# Audio / Voice → SRT
python subtitle_pipeline.py audio recording.wav output/voice.srt

# Plain text → SRT
python subtitle_pipeline.py text "Hello world this is a test." output/text.srt

# Build training dataset
python subtitle_pipeline.py dataset output/subs.srt data/audio.wav --out data/dataset

# Fine-tune Whisper
python subtitle_pipeline.py finetune data/dataset/manifest.json \
    --base-model openai/whisper-small --epochs 3 --out models/finetuned
```

---

## Python API

```python
from subtitle_pipeline import SubtitleMLPipeline

pipeline = SubtitleMLPipeline(whisper_model="small")

# Video → SRT
pipeline.video_to_srt("movie.mp4", "output/movie.srt")

# Audio → SRT
pipeline.audio_to_srt("voice.wav", "output/voice.srt", language="en")

# Text → SRT
pipeline.text_to_srt("Your text here", "output/text.srt", words_per_subtitle=10)

# Build dataset + fine-tune
pipeline.build_dataset("output/movie.srt", "data/audio.wav", "data/dataset")
pipeline.fine_tune("data/dataset/manifest.json", epochs=3)
```

---

## Project Structure

```
subtitle_ml_project/
├── subtitle_pipeline.py       # Main pipeline (all modules)
├── requirements.txt
├── notebooks/
│   └── subtitle_pipeline.ipynb  # Interactive Jupyter notebook
├── data/
│   └── dataset/               # Auto-generated training segments
│       └── manifest.json
├── models/
│   └── whisper-finetuned/     # Saved fine-tuned model
└── output/                    # Generated .srt files
```

---

## Whisper Models

| Model | Parameters | VRAM | Speed |
|---|---|---|---|
| tiny | 39M | ~1 GB | ~32x |
| base | 74M | ~1 GB | ~16x |
| small | 244M | ~2 GB | ~6x |
| medium | 769M | ~5 GB | ~2x |
| large-v3 | 1.5B | ~10 GB | 1x |

---

## Supported Input Formats

- **Video:** `.mp4`, `.mkv`, `.avi`, `.mov`, `.webm`, `.flv`
- **Audio:** `.wav`, `.mp3`, `.flac`, `.ogg`, `.m4a`
- **Text:** plain string, `.txt` file, timestamped JSON, WebVTT

---

## Fine-Tuning Notes

- Uses HuggingFace `Seq2SeqTrainer` with WER metric
- Minimum recommended: ~1 hour of domain-specific audio
- GPU strongly recommended (CUDA or MPS)
- FP16 auto-enabled on CUDA for speed
