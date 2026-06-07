import os, json, subprocess
DEMO=os.path.expanduser("~/runthedocs/series/claude-code/demo"); REC=os.path.join(DEMO,"rec")
term=os.path.join(REC, os.environ.get("CC_TERM","claude-clean.mp4")); bg=os.path.join(REC,"bg45.png")
hook=os.path.join(REC,"hook.png"); narr=os.path.join(REC,"narration.wav")
out=os.path.join(REC, os.environ.get("CC_OUT","claude-ep2-45.mp4"))
TX,TY,TWID=40,170,1000
FF="/opt/homebrew/bin/ffmpeg"; FP="/opt/homebrew/bin/ffprobe"
def dur(p): return float(subprocess.check_output([FP,"-v","error","-show_entries","format=duration","-of","csv=p=0",p]).decode().strip())
VRAW=dur(term)
meta=json.load(open(os.path.join(REC,"narration.json"))); segs=meta["segments"]; n=len(segs)
A=float(meta.get("total") or dur(narr))     # video length = narration length
TAIL=0.8                                      # small breath after last word
DUR=A+TAIL
factor=DUR/VRAW                               # <1 -> speed terminal up to fit
ff=[FF,"-y","-loop","1","-i",bg,"-i",term,"-loop","1","-i",hook]
cap_in={}; nxt=3
for i in range(1,n):
    ff+=["-loop","1","-i",os.path.join(REC,f"cap_{i}.png")]; cap_in[i]=nxt; nxt+=1
ff+=["-i",narr]; audio_idx=nxt
fc=[(f"[1:v]scale={TWID}:-2,tpad=stop_mode=clone:stop_duration={DUR:.2f}[term]" if factor>1.0 else f"[1:v]scale={TWID}:-2,setpts=PTS*{factor:.5f}[term]"),
    f"[0:v][term]overlay={TX}:{TY}[b0]"]
prev="b0"; k=0
hk_end=segs[1]["start"] if n>1 else DUR
k+=1; fc.append(f"[{prev}][2:v]overlay=0:0:enable='between(t,0,{hk_end:.2f})'[s{k}]"); prev=f"s{k}"
for i in range(1,n):
    s=segs[i]["start"]; e=(segs[i+1]["start"] if i+1<n else DUR)
    k+=1; fc.append(f"[{prev}][{cap_in[i]}:v]overlay=0:0:enable='between(t,{s:.2f},{e:.2f})'[s{k}]"); prev=f"s{k}"
ff+=["-filter_complex",";".join(fc),"-map",f"[{prev}]","-map",f"{audio_idx}:a",
     "-t",f"{DUR:.2f}","-r","30","-c:v","libx264","-pix_fmt","yuv420p","-preset","fast","-crf","20",
     "-c:a","aac","-b:a","192k","-movflags","+faststart",out]
print("VRAW=%.2f narration=%.2f DUR=%.2f termSpeed=%.2fx"%(VRAW,A,DUR,1/factor),flush=True)
r=subprocess.run(ff,capture_output=True,text=True)
if r.returncode!=0: print("FFMPEG_FAIL"); print(r.stderr[-1800:]); raise SystemExit(1)
print("COMPOSE45_OK ->",out,flush=True)
