# 다국어 가이드 HTML + 에셋을 website 저장소로 정리
# build/의 4개 HTML과 styles.css를 guides/로, 참조 이미지(8종)를 website/assets/로 (웹용 축소)
import os, shutil
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))          # website/guides
WEB = os.path.dirname(HERE)                                # website
PROJ = os.path.dirname(WEB)                                # Christians Can get Anxious
SRC_BUILD = os.path.join(PROJ, "build")
SRC_ASSETS = os.path.join(PROJ, "assets")
DEST_ASSETS = os.path.join(WEB, "assets")
os.makedirs(DEST_ASSETS, exist_ok=True)

# 1) HTML + styles.css 복사 (한국어 파일은 ASCII 이름으로)
HTML = {
    "Christians_Can_Get_Anxious_EN.html": "Christians_Can_Get_Anxious_EN.html",
    "Christians_Can_Get_Anxious_JA.html": "Christians_Can_Get_Anxious_JA.html",
    "Christians_Can_Get_Anxious_ZH.html": "Christians_Can_Get_Anxious_ZH.html",
    "크리스천도불안_가이드.html":            "Christians_Can_Get_Anxious_KO.html",
}
for src, dst in HTML.items():
    shutil.copyfile(os.path.join(SRC_BUILD, src), os.path.join(HERE, dst))
    print("html:", dst)
shutil.copyfile(os.path.join(SRC_BUILD, "styles.css"), os.path.join(HERE, "styles.css"))
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
