import os, json
from PIL import Image, ImageDraw, ImageFont
DEMO=os.path.expanduser("~/runthedocs/series/claude-code/demo"); REC=os.path.join(DEMO,"rec")
W,H=1080,1920                                 # 9:16 vertical (TikTok / YouTube Shorts / IG Reels)
BG=(10,10,10,255); ACCENT=(218,119,86,255); TEXT=(237,237,237,255); DIM=(150,150,160,255)
_m=json.load(open(os.path.join(REC,"narration.json"))); EP=_m.get("title","CLAUDE CODE"); SUB=_m.get("sub","")
MENLO="/System/Library/Fonts/Menlo.ttc"
def font(sz,idx=0):
    try: return ImageFont.truetype(MENLO,sz,index=idx)
    except: return ImageFont.truetype(MENLO,sz)
def tw(d,s,f): b=d.textbbox((0,0),s,font=f); return b[2]-b[0]
def wrap(d,s,f,maxw):
    out=[]; cur=""
    for w_ in s.split():
        t=(cur+" "+w_).strip()
        (out.append(cur) or 0) if (tw(d,t,f)>maxw and cur) else None
        cur=w_ if (tw(d,t,f)>maxw and cur) else t
    if cur: out.append(cur)
    return out
TX,TY,TWID=40,280,1000
THGT=int(round(TWID*954/1482/2))*2          # ~644, even — same term aspect as 4:5
CAP_CENTER=1240                              # captions centered here (no box; big for mobile)
# ---- static background ----
img=Image.new("RGBA",(W,H),BG); d=ImageDraw.Draw(img)
d.rounded_rectangle([TX-6,TY-6,TX+TWID+6,TY+THGT+6],12,outline=(218,119,86,150),width=2)  # terminal frame
fb=font(26,1); d.ellipse([50,80,68,98],fill=ACCENT); x=80
for ch in "RUN THE DOCS": d.text((x,76),ch,font=fb,fill=ACCENT); x+=tw(d,ch,fb)+4
d.text((50,118),EP,font=font(40,1),fill=TEXT)
d.text((52,166),SUB,font=font(22,0),fill=DIM)
d.line([50,200,1030,200],fill=(218,119,86,90),width=2)   # divider below subtitle
# footer CTA strip
ff=font(32,1); cta="↳  Subscribe — a Claude Code tip every weekday"
d.text(((W-tw(d,cta,ff))//2,1770),cta,font=ff,fill=ACCENT)
ft2=font(24,0); tip="Try it:  "+(_m.get("command") or "claude  → describe a task")
d.text(((W-tw(d,tip,ft2))//2,1828),tip,font=ft2,fill=DIM)
img.save(os.path.join(REC,"bg916.png"))
# ---- segments ----
segs=json.load(open(os.path.join(REC,"narration.json")))["segments"]
# hook overlay (seg 0): dark scrim over terminal + big text
hk=Image.new("RGBA",(W,H),(0,0,0,0)); hd=ImageDraw.Draw(hk)
hd.rounded_rectangle([TX-6,TY-6,TX+TWID+6,TY+THGT+6],12,fill=(8,8,10,225))
fh=font(64,1); lines=wrap(hd,segs[0]["text"],fh,920); lh=78; y=TY+(THGT-lh*len(lines))//2
for ln in lines:
    hd.text(((W-tw(hd,ln,fh))//2,y),ln,font=fh,fill=TEXT); y+=lh
fc=font(26,0); cue="▶  watch"; hd.text(((W-tw(hd,cue,fc))//2,TY+THGT-54),cue,font=fc,fill=ACCENT)
hk.save(os.path.join(REC,"hook916.png"))
# big captions for segs 1..n-1 (no background box — centered in the lower zone)
fcap=font(48,1); MAXW=960
for i in range(1,len(segs)):
    cimg=Image.new("RGBA",(W,H),(0,0,0,0)); cd=ImageDraw.Draw(cimg)
    last=(i==len(segs)-1); col=ACCENT if last else TEXT
    lines=wrap(cd,segs[i]["text"],fcap,MAXW); lh=58; y=CAP_CENTER-(lh*len(lines))//2
    for ln in lines: cd.text(((W-tw(cd,ln,fcap))//2,y),ln,font=fcap,fill=col); y+=lh
    cimg.save(os.path.join(REC,f"cap916_{i}.png"))
print("ASSETS916_OK n=%d thgt=%d"%(len(segs),THGT))
# --- ARTIFACT CARD: a real file -> its contents; otherwise -> the command to type ---
art=_m.get("artifact"); cmd=_m.get("command")
apath=os.path.join(os.environ.get("CC_REPO") or os.path.expanduser("~/runthedocs/series/claude-code/demo/cc-demo-repo"), art or "")
if not (art and os.path.exists(apath)) and cmd:
    aimg=Image.new("RGBA",(W,H),(0,0,0,0)); ad=ImageDraw.Draw(aimg)
    ad.rounded_rectangle([TX-6,TY-6,TX+TWID+6,TY+THGT+6],12,fill=(13,13,18,255))
    ad.rounded_rectangle([TX-6,TY-6,TX+TWID+6,TY+THGT+6],12,outline=ACCENT,width=2)
    fhdr=font(26,1); ad.ellipse([TX+16,TY+18,TX+30,TY+32],fill=ACCENT)
    ad.text((TX+44,TY+14),"the command",font=fhdr,fill=ACCENT)
    ad.line([TX+14,TY+52,TX+TWID-14,TY+52],fill=(218,119,86,90),width=1)
    _p="$ " if (cmd.split()[:1] and cmd.split()[0] in ("git","claude","cat","python3","npm","gh","ls")) else ""
    cmdf=font(40,1); clines=wrap(ad,_p+cmd,cmdf,TWID-60); lh=56
    y=TY+66+max(0,((THGT-72)-lh*len(clines))//2)
    for ln in clines:
        ad.text((TX+30,y),ln,font=cmdf,fill=TEXT); y+=lh
    aimg.save(os.path.join(REC,"artifact916.png")); print("COMMAND CARD 916:",cmd)
elif art and os.path.exists(apath):
    content=open(apath).read().rstrip("\n")
    aimg=Image.new("RGBA",(W,H),(0,0,0,0)); ad=ImageDraw.Draw(aimg)
    ad.rounded_rectangle([TX-6,TY-6,TX+TWID+6,TY+THGT+6],12,fill=(13,13,18,255))
    ad.rounded_rectangle([TX-6,TY-6,TX+TWID+6,TY+THGT+6],12,outline=ACCENT,width=2)
    fhdr=font(26,1); ad.ellipse([TX+16,TY+18,TX+30,TY+32],fill=ACCENT)
    ad.text((TX+44,TY+14),art,font=fhdr,fill=ACCENT)
    ad.line([TX+14,TY+52,TX+TWID-14,TY+52],fill=(218,119,86,90),width=1)
    cf=font(24,0); lh=30; xpad=20; ystart=TY+66
    inner_w=TWID-40; cw=max(1,tw(ad,"M",cf)); maxc=max(8,inner_w//cw)
    ybot=TY+THGT-6; maxlines=max(1,(ybot-ystart)//lh)
    def _hw(s):
        if len(s)<=maxc: return [s]
        ind=len(s)-len(s.lstrip(" ")); pad=" "*min(ind+2,maxc-4)
        out=[]; cur=s
        while len(cur)>maxc:
            cut=cur.rfind(" ",len(pad),maxc)
            if cut<=len(pad): cut=maxc
            out.append(cur[:cut].rstrip())
            cur=pad+cur[cut:].lstrip()
        out.append(cur)
        return out
    rendered=[]
    for ln in content.split("\n"):
        rendered.extend(_hw(ln) if ln else [""])
        if len(rendered)>=maxlines: break
    y=ystart
    for ln in rendered[:maxlines]:
        ad.text((TX+xpad,y),ln,font=cf,fill=TEXT); y+=lh
    aimg.save(os.path.join(REC,"artifact916.png")); print("ARTIFACT CARD 916:",art)
else:
    import pathlib; pathlib.Path(os.path.join(REC,"artifact916.png")).unlink(missing_ok=True)
