import os, json, sys, numpy as np, soundfile as sf, torch, librosa
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
import perth
class _NoWM:
    def apply_watermark(self, wav, sample_rate=None, **k): return wav
    def get_watermark(self, *a, **k): return None
perth.PerthImplicitWatermarker = lambda *a, **k: _NoWM()

DEMO=os.path.expanduser("~/runthedocs/series/claude-code/demo"); REC=os.path.join(DEMO,"rec")
EPFILE=sys.argv[1] if len(sys.argv)>1 else os.path.join(DEMO,"ep2.lines.json")
EP=json.load(open(EPFILE))
LINES=EP["lines"]   # [[display, spoken], ...]
DEV="mps" if torch.backends.mps.is_available() else "cpu"
GAP=0.40; INTRO=0.3; OUTRO=0.6; STRETCH=1.0; EXAG=0.45; CFG=0.5
print("device:",DEV,"episode:",EP.get("title"),flush=True)
m=ChatterboxMultilingualTTS.from_pretrained(device=DEV)
SR=int(getattr(m,"sr",None) or getattr(m,"sample_rate",24000)); print("sr:",SR,flush=True)
def synth(t):
    wav=m.generate(t, language_id="en", audio_prompt_path=None, exaggeration=EXAG, cfg_weight=CFG, temperature=0.7, repetition_penalty=1.2)
    return wav.squeeze().detach().cpu().numpy().astype(np.float32) if hasattr(wav,"squeeze") else np.asarray(wav,dtype=np.float32)
def proc(a):
    a,_=librosa.effects.trim(a,top_db=32)
    if STRETCH!=1.0: a=librosa.effects.time_stretch(a, rate=STRETCH)
    n=int(0.012*SR)
    if len(a)>2*n: a=a.copy(); a[:n]*=np.linspace(0,1,n); a[-n:]*=np.linspace(1,0,n)
    return a.astype(np.float32)
parts=[np.zeros(int(INTRO*SR),dtype=np.float32)]; segs=[]; words=0; speech=0.0
for disp,spk in LINES:
    a=proc(synth(spk)); start=sum(len(x) for x in parts)/SR; parts.append(a); end=sum(len(x) for x in parts)/SR
    segs.append({"text":disp,"start":round(start,3),"end":round(end,3)})
    words+=len(disp.split()); speech+=(end-start)
    parts.append(np.zeros(int(GAP*SR),dtype=np.float32)); print("seg:",disp[:34],"(%.2fs)"%(end-start),flush=True)
parts.append(np.zeros(int(OUTRO*SR),dtype=np.float32))
a=np.concatenate(parts); pk=float(np.max(np.abs(a))) or 1.0; a=a/pk*(10**(-3/20))
sf.write(os.path.join(REC,"narration.wav"),a,SR)
json.dump({"segments":segs,"total":len(a)/SR,"title":EP.get("title"),"sub":EP.get("sub"),"artifact":EP.get("artifact")},open(os.path.join(REC,"narration.json"),"w"),indent=1)
print("CHATTERBOX_NARR_OK total=%.2f WPM=%.0f segs=%d"%(len(a)/SR, words/(speech/60.0), len(segs)),flush=True)
