from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / 'assets'
ROOT.mkdir(exist_ok=True)
points = [(78, 32), (70, 41)]


def curve(x1, y1, x2, y2, x3, y3):
    x0, y0 = points[-1]
    for step in range(1, 33):
        t = step / 32
        u = 1 - t
        points.append((u**3*x0 + 3*u*u*t*x1 + 3*u*t*t*x2 + t**3*x3,
                       u**3*y0 + 3*u*u*t*y1 + 3*u*t*t*y2 + t**3*y3))


curve(65, 36, 59, 34, 53, 34)
curve(40, 34, 32, 43, 32, 55)
curve(32, 67, 41, 75, 53, 75)
curve(60, 75, 65, 73, 69, 70)
points.extend([(69, 60), (53, 60), (53, 49), (81, 49), (81, 76)])
curve(74, 83, 64, 87, 53, 87)
curve(33, 87, 19, 74, 19, 55)
curve(19, 36, 33, 22, 53, 22)
curve(63, 22, 72, 25, 78, 32)
master = Image.new('RGBA', (2048, 2048))
draw = ImageDraw.Draw(master)
draw.ellipse((8, 8, 2040, 2040), fill='#17212b')
draw.polygon([(x * 2048 / 108, y * 2048 / 108) for x, y in points], fill='#e9bb55')
for size in (16, 32, 48, 64, 128, 256, 512):
    for scale in (1, 2):
        name = f'icon{size}' + ('@2x' if scale == 2 else '') + '.png'
        master.resize((size * scale,) * 2, Image.Resampling.LANCZOS).save(ROOT / name)
master.resize((1024, 1024), Image.Resampling.LANCZOS).save(ROOT / 'icon_round512@2x.png')
master.resize((256, 256), Image.Resampling.LANCZOS).save(ROOT / 'icon256.ico', sizes=[(s, s) for s in (16, 24, 32, 48, 64, 128, 256)])
Image.new('RGB', (32, 32), '#151515').save(ROOT / 'background.png')
print('Generated Goldgram icons from the existing Android vector geometry.')
