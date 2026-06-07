import os, json
from PIL import Image, ImageDraw, ImageFont
DEMO=os.path.expanduser("~/runthedocs/series/claude-code/demo"); REC=os.path.join(DEMO,"rec")
W,H=1080,1350
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
TX,TY,TWID=40,170,1000
THGT=int(round(TWID*954/1482/2))*2          # ~644, even
CB_TOP=TY+THGT+22; CB_BOT=1180              # caption band
# ---- static background ----
img=Image.new("RGBA",(W,H),BG); d=ImageDraw.Draw(img)
d.rounded_rectangle([40,CB_TOP,1040,CB_BOT],18,fill=(26,19,16,255))                 # caption band
d.rounded_rectangle([TX-6,TY-6,TX+TWID+6,TY+THGT+6],12,outline=(218,119,86,150),width=2)  # terminal frame
fb=font(26,1); d.ellipse([50,52,68,70],fill=ACCENT); x=80
for ch in "RUN THE DOCS": d.text((x,48),ch,font=fb,fill=ACCENT); x+=tw(d,ch,fb)+4
d.text((50,86),EP,font=font(38,1),fill=TEXT)
d.text((52,132),SUB,font=font(21,0),fill=DIM)
d.line([50,148,1030,148],fill=(218,119,86,90),width=2)
# footer CTA strip
ff=font(30,1); cta="↳  Follow Invotek — daily Claude Code tips"
d.text(((W-tw(d,cta,ff))//2,1245),cta,font=ff,fill=ACCENT)
ft2=font(22,0); tip="Try it:  claude  → describe a task"
d.text(((W-tw(d,tip,ft2))//2,1295),tip,font=ft2,fill=DIM)
img.save(os.path.join(REC,"bg45.png"))
# ---- segments ----
segs=json.load(open(os.path.join(REC,"narration.json")))["segments"]
# hook overlay (seg 0): dark scrim over terminal + big text
hk=Image.new("RGBA",(W,H),(0,0,0,0)); hd=ImageDraw.Draw(hk)
hd.rounded_rectangle([TX-6,TY-6,TX+TWID+6,TY+THGT+6],12,fill=(8,8,10,225))
fh=font(60,1); lines=wrap(hd,segs[0]["text"],fh,900); lh=72; y=TY+(THGT-lh*len(lines))//2
for ln in lines:
    hd.text(((W-tw(hd,ln,fh))//2,y),ln,font=fh,fill=TEXT); y+=lh
# little cue
fc=font(26,0); cue="▶  watch"; hd.text(((W-tw(hd,cue,fc))//2,TY+THGT-54),cue,font=fc,fill=ACCENT)
hk.save(os.path.join(REC,"hook.png"))
# band captions for segs 1..n-1
fcap=font(38,1); MAXW=940
for i in range(1,len(segs)):
    cimg=Image.new("RGBA",(W,H),(0,0,0,0)); cd=ImageDraw.Draw(cimg)
    last=(i==len(segs)-1); col=ACCENT if last else TEXT
    lines=wrap(cd,segs[i]["text"],fcap,MAXW); lh=46; y=CB_TOP+((CB_BOT-CB_TOP)-lh*len(lines))//2
    for ln in lines: cd.text(((W-tw(cd,ln,fcap))//2,y),ln,font=fcap,fill=col); y+=lh
    cimg.save(os.path.join(REC,f"cap_{i}.png"))
print("ASSETS45_OK n=%d thgt=%d"%(len(segs),THGT))
