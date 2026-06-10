import os, json, sys, re, numpy as np, soundfile as sf, torch, librosa
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
INTRA=0.14            # micro-gap between sentences within a line
MAX_TRIES=5
print("device:",DEV,"episode:",EP.get("title"),flush=True)
m=ChatterboxMultilingualTTS.from_pretrained(device=DEV)
SR=int(getattr(m,"sr",None) or getattr(m,"sample_rate",24000)); print("sr:",SR,flush=True)

def gen_raw(t):
    wav=m.generate(t, language_id="en", audio_prompt_path=None, exaggeration=EXAG, cfg_weight=CFG, temperature=0.7, repetition_penalty=1.2)
    return wav.squeeze().detach().cpu().numpy().astype(np.float32) if hasattr(wav,"squeeze") else np.asarray(wav,dtype=np.float32)

def proc(a):
    a,_=librosa.effects.trim(a,top_db=32)
    if STRETCH!=1.0: a=librosa.effects.time_stretch(a, rate=STRETCH)
    n=int(0.012*SR)
    if len(a)>2*n: a=a.copy(); a[:n]*=np.linspace(0,1,n); a[-n:]*=np.linspace(1,0,n)
    return a.astype(np.float32)

def expected_min(text):
    # words * ~0.23s/word (ceiling ~260 WPM); anything shorter is a truncated generation
    w=len(re.findall(r"\w+", text))
    return max(0.7, w*0.23)

def synth_chunk(t):
    # robustly render ONE short sentence: retry until plausibly long, else keep the longest
    target=expected_min(t); best=None
    for k in range(MAX_TRIES):
        a=proc(gen_raw(t)); d=len(a)/SR
        if best is None or d>len(best)/SR: best=a
        if d>=target: return a
        print("   retry [%d] '%s' -> %.2fs < %.2fs"%(k+1,t[:34],d,target),flush=True)
    print("   WARN kept longest %.2fs (<%.2fs) for '%s'"%(len(best)/SR,target,t[:34]),flush=True)
    return best

def synth(spk):
    # split into sentences first — long single calls are what Chatterbox truncates
    sents=[s.strip() for s in re.split(r"(?<=[.!?])\s+", spk.strip()) if s.strip()]
    if len(sents)<=1: return synth_chunk(spk)
    out=[]
    for i,s in enumerate(sents):
        out.append(synth_chunk(s))
        if i<len(sents)-1: out.append(np.zeros(int(INTRA*SR),dtype=np.float32))
    return np.concatenate(out)

parts=[np.zeros(int(INTRO*SR),dtype=np.float32)]; segs=[]; words=0; speech=0.0; bad=0
for disp,spk in LINES:
    a=synth(spk); start=sum(len(x) for x in parts)/SR; parts.append(a); end=sum(len(x) for x in parts)/SR
    dur=end-start; exp=expected_min(spk)
    ok="OK" if dur>=exp else "SHORT"
    if dur<exp: bad+=1
    segs.append({"text":disp,"start":round(start,3),"end":round(end,3)})
    words+=len(disp.split()); speech+=dur
    parts.append(np.zeros(int(GAP*SR),dtype=np.float32)); print("seg:",disp[:34],"(%.2fs, exp>=%.2fs) %s"%(dur,exp,ok),flush=True)
parts.append(np.zeros(int(OUTRO*SR),dtype=np.float32))
a=np.concatenate(parts); pk=float(np.max(np.abs(a))) or 1.0; a=a/pk*(10**(-3/20))
sf.write(os.path.join(REC,"narration.wav"),a,SR)
json.dump({"segments":segs,"total":len(a)/SR,"title":EP.get("title"),"sub":EP.get("sub"),"artifact":EP.get("artifact")},open(os.path.join(REC,"narration.json"),"w"),indent=1)
print("CHATTERBOX_NARR_OK total=%.2f WPM=%.0f segs=%d short_segs=%d"%(len(a)/SR, words/(speech/60.0), len(segs), bad),flush=True)
if bad: print("WARNING: %d segment(s) still under expected length — inspect before publishing"%bad,flush=True)
