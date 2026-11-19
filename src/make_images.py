from PIL import Image, ImageDraw, ImageFont
import os, glob
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'root')
fonts = glob.glob('/usr/share/fonts/**/DejaVuSans-Bold.ttf', recursive=True)
F = lambda s: ImageFont.truetype(fonts[0], s) if fonts else ImageFont.load_default()
def grad(w, h):
    im = Image.new('RGB', (w, h)); d = ImageDraw.Draw(im)
    a, b = (8, 51, 68), (27, 127, 163)
    for y in range(h):
        t = y / h; d.line([(0, y), (w, y)], fill=tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3)))
    return im, d
def boat(d, cx, cy, s, sun=True):
    if sun: d.ellipse([cx + 8*s, cy - 18*s, cx + 18*s, cy - 8*s], fill=(242, 201, 76))
    d.polygon([(cx - 12*s, cy + 5*s), (cx + 12*s, cy + 5*s), (cx + 8*s, cy + 11*s), (cx - 8*s, cy + 11*s)], fill='white')
    d.polygon([(cx - 1*s, cy - 11*s), (cx - 1*s, cy + 4*s), (cx - 10*s, cy + 4*s)], fill='white')
im, d = grad(1200, 630)
d.ellipse([930, -120, 1290, 240], fill=(242, 201, 76))
boat(d, 1010, 430, 9, sun=False)
d.text((80, 170), 'Amalfi Coast', font=F(84), fill='white')
d.text((80, 270), 'Boat Guide', font=F(84), fill=(127, 209, 232))
d.text((80, 400), 'Amalfi Coast & Capri boat tours compared', font=F(36), fill='white')
d.text((80, 455), 'Private vs shared · Positano · Amalfi · Sorrento · Blue Grotto', font=F(26), fill=(207, 227, 234))
d.text((80, 540), 'amalficoastboatguide.com', font=F(28), fill=(242, 201, 76))
im.save(os.path.join(R, 'og.png'), optimize=True)
ic, d = grad(180, 180); boat(d, 85, 95, 5); ic.save(os.path.join(R, 'apple-touch-icon.png'))
