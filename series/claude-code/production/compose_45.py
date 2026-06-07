import os, json, subprocess
DEMO=os.path.expanduser("~/runthedocs/series/claude-code/demo"); REC=os.path.join(DEMO,"rec")
term=os.path.join(REC, os.environ.get("CC_TERM","claude-clean.mp4")); bg=os.path.join(REC,"bg45.png")
hook=os.path.join(REC,"hook.png"); narr=os.path.join(REC,"narration.wav")
out=os.path.join(REC, os.environ.get("CC_OUT","claude-ep2-45.mp4"))

# rc(2026-06-07) COMPOSE GUARD: refuse to compose one episode's terminal over another episode's
# assets/narration. rec/narration.json drives ALL assets+audio; CC_OUT names the episode. This is
# the root cause of the EP1/EP2-rendered-as-EP5 bug — run build-ep.sh <N>, never compose alone.
import re as _re
_want = _re.search(r"ep(\d+)", os.environ.get("CC_OUT","") or os.environ.get("CC_TERM",""))
if _want:
    _title = json.load(open(os.path.join(REC,"narration.json"))).get("title","")
    _got = _re.search(r"EP\s*(\d+)", _title, _re.I)
    if _got and _got.group(1) != _want.group(1):
        raise SystemExit("COMPOSE GUARD: CC_OUT=ep%s but rec/narration.json is '%s' (ep%s). "
                         "Assets/audio belong to a different episode — run build-ep.sh %s, not compose alone."
                         % (_want.group(1), _title, _got.group(1), _want.group(1)))
TX,TY,TWID=40,170,1000
FF="/opt/homebrew/bin/ffmpeg"; FP="/opt/homebrew/bin/ffprobe"
def dur(p): return float(subprocess.check_output([FP,"-v","error","-show_entries","format=duration","-of","csv=p=0",p]).decode().strip())
VRAW=dur(term)
def content_end(p, total):
    # Find where the live terminal stops changing. The dead [terminated] tail is either
    # idle-compressed to ~1s-spaced frames OR a single long-held final frame; live content
    # is dense (<0.7s to the next frame). Keep the last frame quickly followed by another,
    # using the format duration as the sentinel "next" for the final frame.
    try:
        raw=subprocess.check_output([FP,"-v","error","-select_streams","v:0","-show_entries","frame=pts_time","-of","csv=p=0",p]).decode().split()
    except Exception:
        return total
    ts=[]
    for x in raw:
        x=x.strip()
        try: ts.append(float(x))
        except Exception: pass
    ts.sort()
    if len(ts)<3: return total
    GAP=0.7; ext=ts+[total]; live=None
    for i in range(len(ts)):
        if ext[i+1]-ts[i] < GAP: live=i      # frame i is "live": another frame follows quickly
    if live is None: return total
    ce=ts[live]
    return ce if (total*0.3 < ce < total) else total
VEFF=content_end(term, VRAW)
meta=json.load(open(os.path.join(REC,"narration.json"))); segs=meta["segments"]; n=len(segs)
A=float(meta.get("total") or dur(narr))     # video length = narration length
TAIL=0.8                                      # small breath after last word
DUR=A+TAIL
factor=DUR/VEFF                               # <1 -> speed terminal up to fit (over trimmed content only)
artpath=os.path.join(REC,"artifact.png"); has_art=os.path.exists(artpath)
ff=[FF,"-y","-loop","1","-i",bg,"-i",term,"-loop","1","-i",hook]+( ["-loop","1","-i",artpath] if has_art else [] )
ART_IN=3  # index of artifact input (after bg,term,hook)
cap_in={}; nxt=(4 if has_art else 3)
LASTCAP=n-1 if n>3 else -1     # suppress the final outro caption (footer CTA already carries it -> no dup)
for i in range(1,n):
    if i==LASTCAP: continue
    ff+=["-loop","1","-i",os.path.join(REC,f"cap_{i}.png")]; cap_in[i]=nxt; nxt+=1
ff+=["-i",narr]; audio_idx=nxt
TRIM=f"trim=0:{VEFF:.3f},setpts=PTS-STARTPTS,"   # drop the dead [terminated] tail before fitting
fc=[(f"[1:v]{TRIM}scale={TWID}:-2,tpad=stop_mode=clone:stop_duration={DUR:.2f}[term]" if factor>1.0 else f"[1:v]{TRIM}scale={TWID}:-2,setpts=PTS*{factor:.5f}[term]"),
    f"[0:v][term]overlay={TX}:{TY}[b0]"]
prev="b0"; k=0
hk_end=segs[1]["start"] if n>1 else DUR
k+=1; fc.append(f"[{prev}][2:v]overlay=0:0:enable='between(t,0,{hk_end:.2f})'[s{k}]"); prev=f"s{k}"
if has_art:  # ARTIFACT_OVERLAY: show the file card for ~5s after the hook
    a_s=hk_end; a_e=hk_end+5.0
    k+=1; fc.append(f"[{prev}][{ART_IN}:v]overlay=0:0:enable='between(t,{a_s:.2f},{a_e:.2f})'[s{k}]"); prev=f"s{k}"
for i in range(1,n):
    if i==LASTCAP: continue
    s=segs[i]["start"]; e=(segs[i+1]["start"] if i+1<n else DUR)
    k+=1; fc.append(f"[{prev}][{cap_in[i]}:v]overlay=0:0:enable='between(t,{s:.2f},{e:.2f})'[s{k}]"); prev=f"s{k}"
ff+=["-filter_complex",";".join(fc),"-map",f"[{prev}]","-map",f"{audio_idx}:a",
     "-t",f"{DUR:.2f}","-r","30","-c:v","libx264","-pix_fmt","yuv420p","-preset","fast","-crf","20",
     "-c:a","aac","-b:a","192k","-ar","48000","-ac","2","-movflags","+faststart",out]
print("VRAW=%.2f VEFF=%.2f narration=%.2f DUR=%.2f termSpeed=%.2fx"%(VRAW,VEFF,A,DUR,1/factor),flush=True)
r=subprocess.run(ff,capture_output=True,text=True)
if r.returncode!=0: print("FFMPEG_FAIL"); print(r.stderr[-1800:]); raise SystemExit(1)
print("COMPOSE45_OK ->",out,flush=True)
