# 웹용 이미지 최적화 스크립트
# 원본(../assets)을 읽어 website/assets/img 에 ASCII 파일명 + 적정 크기로 저장
# 실행: python build_assets.py
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "assets"))
OUT = os.path.join(HERE, "assets", "img")
os.makedirs(OUT, exist_ok=True)


def resize_max(im, maxw):
    if im.width > maxw:
        h = int(im.height * maxw / im.width)
        im = im.resize((maxw, h), Image.LANCZOS)
    return im


def square_crop(im, size, top_bias=0.15):
    """가로 중앙 + 세로는 약간 위쪽으로 치우쳐 정사각 크롭 (얼굴 보존)."""
    w, h = im.size
    side = min(w, h)
    left = (w - side) // 2
    top = int((h - side) * top_bias)
    im = im.crop((left, top, left + side, top + side))
    return im.resize((size, size), Image.LANCZOS)


# (소스경로, 출력파일명, 최대폭, 포맷)
JOBS = [
    ("Studio Grade Book Photos/Book_Background Removed.png", "book-cover.png", 900, "PNG"),
    ("Studio Grade Book Photos/Book_On Table with Candle.png", "book-candle.jpg", 1500, "JPEG"),
    ("Profile Photos/Photo_이기원_Background Removed.png", "author-lee.png", 560, "PNG"),
    ("Profile Photos/Photo_채규만_Background Removed.png", "author-chae-gm.png", 560, "PNG"),
    ("Profile Photos/Photo_채정호_Background Removed.png", "author-chae-jh.png", 560, "PNG"),
    ("Hands Grabbing.png", "hands.jpg", 1400, "JPEG"),
]

# 추천인 원형 프로필 (정사각 크롭)
RECS = [
    ("Profile Photos/이재훈.webp", "rec-jaehoon.jpg"),
    ("Profile Photos/이찬수.jpg",  "rec-chansoo.jpg"),
    ("Profile Photos/권수영.png",  "rec-sooyoung.jpg"),
    ("Profile Photos/박재연.png",  "rec-jaeyeon.jpg"),
    ("Profile Photos/이강학.jpg",  "rec-ganghak.jpg"),
    ("Profile Photos/이영표.jpg",  "rec-youngpyo.jpg"),
]

for rel, name, maxw, fmt in JOBS:
    src = os.path.join(SRC, rel)
    if not os.path.exists(src):
        print(f"!! 없음: {src}"); continue
    im = resize_max(Image.open(src), maxw)
    dst = os.path.join(OUT, name)
    if fmt == "JPEG":
        im.convert("RGB").save(dst, "JPEG", quality=85, optimize=True)
    else:
        im.save(dst, "PNG", optimize=True)
    print(f"saved: {name}  ({im.width}x{im.height}, {os.path.getsize(dst)//1024}KB)")

for rel, name in RECS:
    src = os.path.join(SRC, rel)
    if not os.path.exists(src):
        print(f"!! 없음: {src}"); continue
    im = square_crop(Image.open(src).convert("RGB"), 360)
    dst = os.path.join(OUT, name)
    im.save(dst, "JPEG", quality=86, optimize=True)
    print(f"saved: {name}  (360x360, {os.path.getsize(dst)//1024}KB)")

print("완료")
