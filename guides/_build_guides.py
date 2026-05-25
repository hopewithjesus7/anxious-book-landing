# 가이드(티저) HTML + 에셋을 website 저장소로 정리
# 정책 변경(2026-05): 저작권 우려로 상세 다국어 풀가이드는 내리고,
# 한국어 티저(약 25% 축약본) 한 종만 guides/index.html 로 게시.
# build/크리스천도불안_25.html → guides/index.html, styles.css 복사, 참조 이미지(8종)를 website/assets/로 축소 복사.
import os, shutil
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))          # website/guides
WEB = os.path.dirname(HERE)                                # website
PROJ = os.path.dirname(WEB)                                # Christians Can get Anxious
SRC_BUILD = os.path.join(PROJ, "build")
SRC_ASSETS = os.path.join(PROJ, "assets")
DEST_ASSETS = os.path.join(WEB, "assets")
os.makedirs(DEST_ASSETS, exist_ok=True)

# 1) 티저 HTML(한국어 25%) → guides/index.html, styles.css 복사
shutil.copyfile(os.path.join(SRC_BUILD, "크리스천도불안_25.html"), os.path.join(HERE, "index.html"))
shutil.copyfile(os.path.join(SRC_BUILD, "styles.css"), os.path.join(HERE, "styles.css"))
print("html: index.html (한국어 티저)")
print("css: styles.css")

# 2) 참조 이미지 8종을 웹용으로 축소 복사 (파일명 그대로 유지 — HTML이 정확히 참조)
IMGS = [
    ("Mongle_Heart Eyes.png", 700), ("Mongle_Shining Eyes.png", 700),
    ("Mongle_Base.png", 700), ("Mongle_Surpirsed.png", 700),
    ("Mongle_Crying.png", 700), ("Mongle_Happy v1.png", 700),
    ("Mongle_Happy v2.png", 700), ("Book_Clean White Background.png", 900),
]
for name, maxw in IMGS:
    src = os.path.join(SRC_ASSETS, name)
    if not os.path.exists(src):
        print("!! 없음:", name); continue
    im = Image.open(src)
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    dst = os.path.join(DEST_ASSETS, name)
    im.save(dst, "PNG", optimize=True)
    print(f"img: {name}  ({im.width}x{im.height}, {os.path.getsize(dst)//1024}KB)")

print("완료")
