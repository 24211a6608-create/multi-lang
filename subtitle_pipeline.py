from pathlib import Path
from dataclasses import dataclass, field
from typing import List
from deep_translator import GoogleTranslator

# ---------- DATA STRUCTURES ----------

@dataclass
class SubtitleEntry:
    index:int
    start:float
    end:float
    text:str

    def fmt(self,s):
        h,m=int(s//3600),int((s%3600)//60)
        return f"{h:02}:{m:02}:{int(s%60):02},{int((s-int(s))*1000):03}"

    def to_srt(self):
        return f"{self.index}\n{self.fmt(self.start)} --> {self.fmt(self.end)}\n{self.text}\n"

@dataclass
class TranscriptionResult:
    entries:List[SubtitleEntry]=field(default_factory=list)
    def to_srt(self):
        return "\n".join(e.to_srt() for e in self.entries)

# ---------- WHISPER ----------

class WhisperTranscriber:
    def __init__(self,model="base"):
        self.name=model
        self.model=None
    def _load(self):
        if not self.model:
            import whisper
            self.model=whisper.load_model(self.name)
    def transcribe(self,audio,language=None):
        self._load()
        opts={"verbose":False}
        if language: opts["language"]=language
        r=self.model.transcribe(audio,**opts)
        entries=[]
        for i,seg in enumerate(r["segments"]):
            entries.append(SubtitleEntry(i+1,seg["start"],seg["end"],seg["text"].strip()))
        return TranscriptionResult(entries)

# ---------- TRANSLATOR ----------

LANG_CODES={
    "English":"en","Hindi":"hi","Bengali":"bn","Tamil":"ta",
    "Telugu":"te","Marathi":"mr","Urdu":"ur"
}

class Translator:
    def translate(self,text,target_lang):
        try:
            code=LANG_CODES.get(target_lang,"en")
            return GoogleTranslator(source="auto",target=code).translate(text)
        except:
            return text

# ---------- TEXT ----------

class TextToSRT:
    def convert(self,text,words=10):
        w=text.split();entries=[];t=0;i=1
        for j in range(0,len(w),words):
            chunk=" ".join(w[j:j+words])
            dur=max(3,len(chunk.split())*0.4)
            entries.append(SubtitleEntry(i,t,t+dur,chunk))
            t+=dur;i+=1
        return TranscriptionResult(entries)

# ---------- PIPELINE ----------

class SubtitleMLPipeline:
    supported_languages=list(LANG_CODES.keys())
    def __init__(self,model="base"):
        self.transcriber=WhisperTranscriber(model)
        self.translator=Translator()
        self.text_conv=TextToSRT()

    def _save(self,res,path):
        Path(path).write_text(res.to_srt(),encoding="utf-8")

    def _translate(self,res,lang):
        for e in res.entries:
            e.text=self.translator.translate(e.text,lang)
        return res

    def audio_to_srt(self,audio,out,language=None,target_lang=None):
        res=self.transcriber.transcribe(audio,language)
        if target_lang and target_lang!="No Translation":
            res=self._translate(res,target_lang)
        self._save(res,out)
        return res

    def text_to_srt(self,text,out,words=10,target_lang=None):
        res=self.text_conv.convert(text,words)
        if target_lang and target_lang!="No Translation":
            res=self._translate(res,target_lang)
        self._save(res,out)
        return res