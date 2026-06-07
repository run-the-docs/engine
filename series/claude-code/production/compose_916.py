import os, json, subprocess
DEMO=os.path.expanduser("~/runthedocs/series/claude-code/demo"); REC=os.path.join(DEMO,"rec")
term=os.path.join(REC, os.environ.get("CC_TERM","claude-clean.mp4")); bg=os.path.join(REC,"bg916.png")
hook=os.path.join(REC,"hook916.png"); narr=os.path.join(REC,"narration.wav")
out=os.path.join(REC, os.environ.get("CC_OUT","claude-ep2-916.mp4"))
TX,TY,TWID=40,280,1000
FF="/opt/homebrew/bin/ffmpeg"; FP="/opt/homebrew/bin/ffprobe"
def dur(p): return float(subprocess.check_output([FP,"-v","error","-show_entries","format=duration","-of","csv=p=0",p]).decode().strip())
VRAW=dur(term)
def content_end(p, total):
    # Trim the dead [terminated] tail: keep the last frame quickly followed by another
    # (live content <0.7s apart; the dead tail is idle-compressed or a long-held final frame).
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
        if ext[i+1]-ts[i] < GAP: live=i
    if live is None: return total
    ce=ts[live]
    return ce if (total*0.3 < ce < total) else total
VEFF=content_end(term, VRAW)
meta=json.load(open(os.path.join(REC,"narration.json"))); segs=meta["segments"]; n=len(segs)
A=float(meta.get("total") or dur(narr))     # video length = narration length
TAIL=0.8
DUR=A+TAIL
factor=DUR/VEFF
artpath=os.path.join(REC,"artifact916.png"); has_art=os.path.exists(artpath)
ff=[FF,"-y","-loop","1","-i",bg,"-i",term,"-loop","1","-i",hook]+( ["-loop","1","-i",artpath] if has_art else [] )
ART_IN=3
cap_in={}; nxt=(4 if has_art else 3)
LASTCAP=n-1 if n>3 else -1     # suppress final outro caption (footer CTA carries it)
for i in range(1,n):
    if i==LASTCAP: continue
    ff+=["-loop","1","-i",os.path.join(REC,f"cap916_{i}.png")]; cap_in[i]=nxt; nxt+=1
ff+=["-i",narr]; audio_idx=nxt
TRIM=f"trim=0:{VEFF:.3f},setpts=PTS-STARTPTS,"
fc=[(f"[1:v]{TRIM}scale={TWID}:-2,tpad=stop_mode=clone:stop_duration={DUR:.2f}[term]" if factor>1.0 else f"[1:v]{TRIM}scale={TWID}:-2,setpts=PTS*{factor:.5f}[term]"),
    f"[0:v][term]overlay={TX}:{TY}[b0]"]
prev="b0"; k=0
hk_end=segs[1]["start"] if n>1 else DUR
k+=1; fc.append(f"[{prev}][2:v]overlay=0:0:enable='between(t,0,{hk_end:.2f})'[s{k}]"); prev=f"s{k}"
if has_art:
    a_s=hk_end; a_e=hk_end+5.0
    k+=1; fc.append(f"[{prev}][{ART_IN}:v]overlay=0:0:enable='between(t,{a_s:.2f},{a_e:.2f})'[s{k}]"); prev=f"s{k}"
for i in range(1,n):
    if i==LASTCAP: continue
    s=segs[i]["start"]; e=(segs[i+1]["start"] if i+1<n else DUR)
    k+=1; fc.append(f"[{prev}][{cap_in[i]}:v]overlay=0:0:enable='between(t,{s:.2f},{e:.2f})'[s{k}]"); prev=f"s{k}"
ff+=["-filter_complex",";".join(fc),"-map",f"[{prev}]","-map",f"{audio_idx}:a",
     "-t",f"{DUR:.2f}","-r","30","-c:v","libx264","-pix_fmt","yuv420p","-preset","fast","-crf","20",
     "-c:a","aac","-b:a","192k","-movflags","+faststart",out]
print("VRAW=%.2f VEFF=%.2f narration=%.2f DUR=%.2f termSpeed=%.2fx"%(VRAW,VEFF,A,DUR,1/factor),flush=True)
r=subprocess.run(ff,capture_output=True,text=True)
if r.returncode!=0: print("FFMPEG_FAIL"); print(r.stderr[-1800:]); raise SystemExit(1)
print("COMPOSE916_OK ->",out,flush=True)
