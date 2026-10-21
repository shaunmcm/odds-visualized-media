import subprocess, sys
from PIL import Image
for v in sys.argv[1:]:
    ims=[]
    for t in ['0.3','3','5.5','8.5','13']:
        p=f'frames/{v}_{t}.png'
        subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',t,'-i',f'out/{v}.mp4','-frames:v','1','-vf','scale=240:-1',p],check=True)
        ims.append(Image.open(p))
    c=Image.new('RGB',(sum(i.width for i in ims)+40,ims[0].height),(80,80,80));x=0
    for i in ims: c.paste(i,(x,0)); x+=i.width+10
    c.save(f'frames/{v}_strip.png')
