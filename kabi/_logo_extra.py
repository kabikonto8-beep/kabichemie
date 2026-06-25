# -*- coding: utf-8 -*-
"""Biała wersja napisu (na pasek nad wideo) + favicon z sygnetu."""
from PIL import Image, ImageDraw

def white_version(src, dst):
    im = Image.open(src).convert('RGBA')
    a = im.split()[3]
    L = Image.new('L', im.size, 255)
    Image.merge('RGBA', (L, L, L, a)).save(dst)
    print('zapisano', dst, im.size)

# biały napis (KABICHEMIE WATER TREATMENT) na ciemne tło
white_version('src/assets/logo-word.png', 'src/assets/logo-word-white.png')

# --- favicon: granatowy zaokrąglony kwadrat + biały sygnet ---
mark = Image.open('src/assets/logo-mark.png').convert('RGBA')
ma = mark.split()[3]
Lm = Image.new('L', mark.size, 255)
mark_white = Image.merge('RGBA', (Lm, Lm, Lm, ma))

S = 64
fav = Image.new('RGBA', (S, S), (0, 0, 0, 0))
ImageDraw.Draw(fav).rounded_rectangle([0, 0, S - 1, S - 1], radius=14, fill=(11, 61, 92, 255))
mw, mh = mark_white.size
sc = 42 / max(mw, mh)
mr = mark_white.resize((max(1, int(mw * sc)), max(1, int(mh * sc))), Image.LANCZOS)
fav.alpha_composite(mr, ((S - mr.size[0]) // 2, (S - mr.size[1]) // 2))
fav.save('src/assets/favicon.png')
print('zapisano favicon.png', fav.size)
