"""
JooN's Sushi TV - v8.0 (Food Quotes + Sushi BG / Person Quotes + Portrait BG)
"""
import json, os, re, base64, random
from menu_utils import find_local_image, img_to_base64

MENU_JSON  = "menu.json"
IMAGE_DIR  = "images"
OUTPUT_HTML= "index.html"

# 음식 관련 태그 (이 태그 → 스시 이미지 배경)
FOOD_TAGS = {"food", "sushi", "chef", "health", "history", "salmon"}

# 인물 초상화 매핑 (본인 전용 이미지)
WHO_TO_BG = {
    # 기존 초상화
    "SOCRATES":           "인물/bg_socrates.png",
    "ARISTOTLE":          "인물/bg_aristotle.png",
    "EINSTEIN":           "인물/bg_einstein.png",
    "HIPPOKRATES":        "인물/bg_hippokrates.png",
    "LAO TZU":            "인물/bg_laotzu.png",
    "CONFUCIUS":          "인물/bg_confucius.png",
    "CONFUCUIUS":         "인물/bg_confucius.png",
    "STEVE JOBS":         "인물/bg_jobs.png",
    "MAHATMA GANDHI":     "인물/bg_gandhi.png",
    "BRUCE LEE":          "인물/bg_brucelee.png",
    "ZEN WISDOM":         "bg_zen.png",
    "DALAI LAMA":         "bg_zen.png",
    "KOREAN PROVERB":     "bg_scholar.png",
    # Canva AI 생성 초상화
    "FRIEDRICH NIETZSCHE": "인물/bg_nietzsche.png",
    "PLATO":              "인물/bg_plato.png",
    "WINSTON CHURCHILL":  "인물/bg_churchill.png",
    "BENJAMIN FRANKLIN":  "인물/bg_franklin.png",
    "MARK TWAIN":         "인물/bg_marktwain.png",
    "PABLO PICASSO":      "인물/bg_picasso.png",
    "LEONARDO DA VINCI":  "인물/bg_davinci.png",
    "MARCUS AURELIUS":    "인물/bg_marcusaurelius.png",
    "HENRY FORD":         "인물/bg_henryford.png",
    "HELEN KELLER":       "인물/bg_helenkeller.png",
    "MAYA ANGELOU":       "인물/bg_mayaangelou.png",
    "RUMI":               "인물/bg_rumi.jpg",
    "RAY DALIO":          "인물/bg_dalio.jpg",
    "SUSHI MASTER":       "bg_sushi_master.png",
    "SHOKUNIN":           "bg_sushi_master.png",
    "CHEF":               "bg_chef.png",
    # 추가 초상화 (10명)
    "ANNE FRANK":         "인물/bg_annefrank.png",
    "SENECA":             "인물/bg_seneca.png",
    "OSCAR WILDE":        "인물/bg_oscarwilde.png",
    "VINCENT VAN GOGH":   "인물/bg_vangogh.png",
    "EPICURUS":           "인물/bg_epicurus.png",
    "WAYNE GRETZKY":      "인물/bg_gretzky.png",
    "NAPOLEON HILL":      "인물/bg_napoleonhill.png",
    "JIM ROHN":           "인물/bg_jimrohn.png",
    "MARIE MODIANO":      "인물/bg_mariemodiano.png",
    "ST. AUGUSTINE":      "인물/bg_staugustine.png",
}

# 인물 초상화 색상
PORTRAIT_COLORS = {
    "인물/bg_socrates.png":     {"accent": "#00FF9D", "atmos": "#0A2F1F"},
    "인물/bg_aristotle.png":    {"accent": "#00E5FF", "atmos": "#0A1A2F"},
    "인물/bg_einstein.png":     {"accent": "#BB86FC", "atmos": "#1A0A2F"},
    "인물/bg_hippokrates.png":  {"accent": "#76FF03", "atmos": "#0F2F0A"},
    "인물/bg_laotzu.png":       {"accent": "#FFD54F", "atmos": "#2F1A0A"},
    "인물/bg_confucius.png":    {"accent": "#FFEA00", "atmos": "#2F2F0A"},
    "인물/bg_jobs.png":         {"accent": "#FFFFFF", "atmos": "#0A0A0A"},
    "인물/bg_gandhi.png":       {"accent": "#FFAB40", "atmos": "#2F1F0A"},
    "인물/bg_brucelee.png":     {"accent": "#FF1744", "atmos": "#2F0A0A"},
    "bg_zen.png":          {"accent": "#B2FF59", "atmos": "#0A1F0F"},
    "bg_scholar.png":      {"accent": "#80D8FF", "atmos": "#0A1F2F"},
    "인물/bg_nietzsche.png":    {"accent": "#FF8A65", "atmos": "#1A0A05"},
    "인물/bg_plato.png":        {"accent": "#FFD54F", "atmos": "#1A1A0A"},
    "인물/bg_churchill.png":    {"accent": "#90CAF9", "atmos": "#0A0F1A"},
    "인물/bg_franklin.png":     {"accent": "#FFB74D", "atmos": "#1A0F05"},
    "인물/bg_marktwain.png":    {"accent": "#BCAAA4", "atmos": "#1A0F0A"},
    "인물/bg_picasso.png":      {"accent": "#CE93D8", "atmos": "#1A0A1A"},
    "인물/bg_davinci.png":      {"accent": "#A1887F", "atmos": "#1A0F0A"},
    "인물/bg_marcusaurelius.png": {"accent": "#FFD700", "atmos": "#1A1A05"},
    "인물/bg_henryford.png":    {"accent": "#B0BEC5", "atmos": "#0A0F1A"},
    "인물/bg_helenkeller.png":  {"accent": "#F48FB1", "atmos": "#1A0A0F"},
    "인물/bg_mayaangelou.png":  {"accent": "#FFB300", "atmos": "#1A0F05"},
    "인물/bg_rumi.jpg":         {"accent": "#FFD54F", "atmos": "#1A0F05"},
    "인물/bg_dalio.jpg":        {"accent": "#8AB1FF", "atmos": "#050A1A"}, # Gemini Nano Style
    "bg_sushi_master.png": {"accent": "#FFD54F", "atmos": "#0A0A0A"},
    "bg_chef.png":         {"accent": "#C9A96E", "atmos": "#0F0F0F"},
    "인물/bg_annefrank.png":    {"accent": "#FFB74D", "atmos": "#1A0F05"},
    "인물/bg_seneca.png":       {"accent": "#CD853F", "atmos": "#1A0A05"},
    "인물/bg_oscarwilde.png":   {"accent": "#CE93D8", "atmos": "#1A0A1A"},
    "인물/bg_vangogh.png":      {"accent": "#FFD700", "atmos": "#0A0F1A"},
    "인물/bg_epicurus.png":     {"accent": "#FFB74D", "atmos": "#1A0F0A"},
    "인물/bg_gretzky.png":      {"accent": "#90CAF9", "atmos": "#0A0A1A"},
    "인물/bg_napoleonhill.png": {"accent": "#FFB74D", "atmos": "#1A0F05"},
    "인물/bg_jimrohn.png":      {"accent": "#FFB300", "atmos": "#1A0F05"},
    "인물/bg_mariemodiano.png": {"accent": "#F48FB1", "atmos": "#1A0A0F"},
    "인물/bg_staugustine.png":  {"accent": "#FFD54F", "atmos": "#1A0F0A"},
}

# 카테고리별 전용 배경 이미지 + 색상
CATEGORY_BG = {
    "history":    {"file": "bg_history.png",    "accent": "#FFB74D", "atmos": "#1A0F05"},
    "science":    {"file": "bg_science.png",    "accent": "#00E5FF", "atmos": "#050A1A"},
    "psychology": {"file": "bg_psychology.png", "accent": "#CE93D8", "atmos": "#0F051A"},
    "economics":  {"file": "인물/bg_dalio.jpg",       "accent": "#8AB1FF", "atmos": "#051A0A"},
}

# 음식 명언 배경 색상 (스시 이미지용 - 따뜻한 골드 톤)
FOOD_ACCENT = {"accent": "#C9A96E", "atmos": "#0A0A0E"}

CAT_COLORS = {
    "APPETIZERS": "#FF4081", "SPECIAL ROLLS": "#FF6E40",
    "SUSHI": "#00E5FF", "SASHIMI": "#76FF03",
    "ENTREE": "#FFEA00",
}

to_b64 = img_to_base64
find_menu_img = find_local_image

# 음식 명언 키워드 → 배경 이미지 매칭
FOOD_KEYWORDS = {
    "sushi":  {"words": ["sushi", "roll", "nori", "born from the sea", "experience"],
               "prefix": "bg_kw_sushi_"},
    "salmon": {"words": ["salmon"],
               "prefix": "bg_kw_salmon_"},
    "chef":   {"words": ["cook", "chef", "craft", "kitchen", "skill", "ingredient",
                         "basics", "balance", "journey", "repeat", "elevate", "transform"],
               "prefix": "bg_kw_chef_"},
    "health": {"words": ["health", "medicine", "body", "moderation", "wealth", "you are what"],
               "prefix": "bg_kw_health_"},
    "food":   {"words": ["food", "eat", "dine", "taste", "flavor", "fresh", "mood",
                         "king", "symphony", "love of food"],
               "prefix": "bg_kw_food_"},
}

def find_keyword_bg(quote_en):
    """명언 텍스트에서 키워드 매칭하여 해당 배경 이미지 반환"""
    en_lower = quote_en.lower()
    for kw, info in FOOD_KEYWORDS.items():
        if any(w in en_lower for w in info["words"]):
            prefix = info["prefix"]
            matches = sorted([f for f in os.listdir(".") if f.startswith(prefix) and f.endswith(".jpg")])
            if matches:
                return matches
    return None

def build():
    # 메뉴 로드
    with open(MENU_JSON, "r", encoding="utf-8") as f:
        all_items = json.load(f)
    
    cats = {}
    for item in all_items:
        img_path = find_menu_img(item["name"])
        if img_path:
            item["img_b64"] = to_b64(img_path)
            cats.setdefault(item["category"].strip(), []).append(item)
    
    # 명언 로드 - 메인 + 하위 폴더 전체
    wisdom_list = []
    wisdom_dir = "wisdom_data"
    # 메인 quotes.json
    main_path = os.path.join(wisdom_dir, "quotes.json")
    if os.path.exists(main_path):
        with open(main_path, "r", encoding="utf-8") as f:
            wisdom_list.extend(json.load(f))
    # 하위 폴더 (history, science, psychology, economics)
    for sub in os.listdir(wisdom_dir):
        sub_path = os.path.join(wisdom_dir, sub, "quotes.json")
        if os.path.isdir(os.path.join(wisdom_dir, sub)) and os.path.exists(sub_path):
            with open(sub_path, "r", encoding="utf-8") as f:
                wisdom_list.extend(json.load(f))
    random.shuffle(wisdom_list)
    print(f"명언 총: {len(wisdom_list)}개")

    # 이미지 명언 로드 (quotes/ 폴더, 파일 참조 방식 — base64 인코딩 안 함)
    quote_img_dir = "quotes"
    quote_images = []
    if os.path.isdir(quote_img_dir):
        quote_images = sorted([f for f in os.listdir(quote_img_dir)
                               if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
        random.shuffle(quote_images)
    print(f"이미지 명언: {len(quote_images)}장")
    QUOTE_BATCH = 3  # 자리당 연속 재생 장수 (메뉴 광고 비중 우선)
    quote_queue = list(quote_images)

    # 프로모션 이미지 로드 (promos/ 폴더)
    promo_img_dir = "promos"
    promo_images = []
    if os.path.isdir(promo_img_dir):
        promo_images = sorted([f for f in os.listdir(promo_img_dir)
                               if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
        random.shuffle(promo_images)
    print(f"프로모션 이미지: {len(promo_images)}장")
    PROMO_PER_SLOT = 1  # 자리당 프로모션 장수 (명언 앞에 삽입)
    promo_queue = list(promo_images)

    from urllib.parse import quote as _urlq
    def make_quote_img_slide(fname):
        url = "quotes/" + _urlq(fname)
        return (
            f'<div class="slide slide-quote-img">'
            f'<div class="qimg-bg" style="background-image:url(\'{url}\')"></div>'
            f'</div>'
        )

    def make_promo_img_slide(fname):
        url = "promos/" + _urlq(fname)
        return (
            f'<div class="slide slide-quote-img slide-promo-img">'
            f'<div class="qimg-bg" style="background-image:url(\'{url}\')"></div>'
            f'</div>'
        )

    def pop_slot_slides():
        """자리 1개 = 프로모션 N장 + 명언 M장 (큐 비면 스킵)"""
        out = []
        for _ in range(PROMO_PER_SLOT):
            if promo_queue:
                out.append(make_promo_img_slide(promo_queue.pop(0)))
        for _ in range(QUOTE_BATCH):
            if quote_queue:
                out.append(make_quote_img_slide(quote_queue.pop(0)))
        return out

    # Pixabay 스시 이미지를 음식 명언 배경으로 사용
    sushi_bg_images = sorted([f for f in os.listdir(".") if f.startswith("bg_sushi_") and f.endswith(".jpg")])
    if not sushi_bg_images:
        # fallback: 메뉴 이미지 사용
        sushi_bg_images = [os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR)
                           if f.lower().endswith('.jpg')]
    random.shuffle(sushi_bg_images)
    sushi_bg_idx = 0
    cat_counters = {}
    used_once = set()      # 초상화/카테고리 - 절대 재사용 금지
    used_sushi = set()     # 스시 이미지 - 소진 시 리셋 허용

    # 배경 이미지 B64 캐시
    bg_cache = {}
    def get_bg_b64(path):
        if path not in bg_cache:
            bg_cache[path] = to_b64(path)
        return bg_cache[path]

    slides = []
    wisdom_idx = 0
    web_idx = 0

    # 커버 슬라이드
    cover_b64  = to_b64("bg_cover.png")
    title_b64  = to_b64("bg_title.png")
    menu_b64   = to_b64("bg_menu.png")

    slides.append(
        f'<div class="slide slide-title active" data-accent="#C9A96E" data-atmos="#060609"'
        f' style="background-image:url(\'{cover_b64}\');background-size:cover;background-position:center;">'
        '<div class="cover-wrap">'
        '<div class="cover-title">JooN\'s Sushi</div>'
        '<div class="cover-sub">— M E N U —</div>'
        '<div class="cover-line"></div>'
        '<div class="cover-addr">29910 Murrieta Hot Springs Rd L, Murrieta, CA</div>'
        '</div>'
        '</div>'
    )

    # 커버 직후 프로모션 + 명언 batch
    slides.extend(pop_slot_slides())

    for cat, items in cats.items():
        accent = CAT_COLORS.get(cat.upper(), "#C9A96E")

        # 카테고리 타이틀 슬라이드 (3초)
        slides.append(
            f'<div class="slide slide-title" data-accent="{accent}" data-atmos="#050810"'
            f' style="background-image:url(\'{title_b64}\');background-size:cover;background-position:center;">'
            f'<div class="cover-wrap">'
            f'<div class="title-cat" style="color:{accent}">{cat}</div>'
            f'<div class="title-sub" style="color:{accent}">✦ {len(items)} Selections ✦</div>'
            f'</div>'
            f'</div>'
        )

        # 메뉴 아이템 (3개씩, 3초)
        for i in range(0, len(items), 3):
            chunk = items[i:i+3]
            cards_html = ""
            for it in chunk:
                cards_html += (
                    f'<div class="card" style="border-color:{accent}55">'
                    f'<div class="card-img"><img src="{it["img_b64"]}" alt="{it["name"]}"></div>'
                    f'<div class="card-body">'
                    f'<div class="card-name">{it["name"]}</div>'
                    f'<div class="card-price" style="color:{accent}">{it["price"]}</div>'
                    f'</div></div>'
                )
            slides.append(
                f'<div class="slide slide-menu" data-accent="{accent}" data-atmos="#000000"'
                f' style="background-image:url(\'{menu_b64}\');background-size:cover;background-position:center;">'
                f'<div class="menu-header"><span style="color:{accent}">{cat}</span></div>'
                f'<div class="cards cards-{len(chunk)}">{cards_html}</div>'
                f'</div>'
            )

            # 메뉴 슬라이드 사이에 프로모션 + 명언 batch
            slides.extend(pop_slot_slides())

    html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>JooN's Sushi Menu</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&family=Cormorant+Garamond:wght@700&family=Inter:wght@300;400&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{width:100vw;height:100vh;overflow:hidden;background:#060609;color:#F0EDE6;font-family:'Inter',sans-serif;cursor:none;}
.slideshow{position:relative;width:100vw;height:100vh;}
.slide{position:absolute;inset:0;opacity:0;transition:opacity 1.2s ease;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.slide.active{opacity:1;z-index:10;}

/* 커버 & 타이틀 */
.cover-wrap{text-align:center;}
.cover-title{font-family:'Playfair Display';font-size:110px;letter-spacing:8px;color:#C9A96E;}
.cover-sub{font-size:22px;letter-spacing:18px;color:#C9A96E;opacity:0.8;margin-top:20px;margin-bottom:30px;}
.cover-line{width:250px;height:1px;background:rgba(201,169,110,0.5);margin:0 auto 30px auto;}
.cover-addr{font-size:15px;letter-spacing:5px;color:#C9A96E;font-weight:300;}
.title-cat{font-family:'Cormorant Garamond';font-size:52px;letter-spacing:10px;text-transform:uppercase;white-space:nowrap;text-shadow:0 0 40px rgba(0,0,0,0.9),0 0 80px rgba(0,0,0,0.7);}
.title-sub{font-size:22px;letter-spacing:12px;margin-top:20px;border-top:1.5px solid;padding-top:20px;text-shadow:0 0 20px rgba(0,0,0,0.8);}
.slide-title{background:#050810;}

/* 메뉴 카드 - TV overscan safe area (5% 여백) */
.slide-menu{background:#000;justify-content:flex-start;padding:4vh 5vw 4vh 5vw;}
.menu-header{font-family:'Cormorant Garamond';font-size:clamp(28px,3.5vmin,48px);letter-spacing:10px;text-transform:uppercase;margin-bottom:2.5vh;text-align:center;}
.cards{display:flex;gap:2.5vw;justify-content:center;padding:0;}
.card{border:1px solid;border-radius:18px;overflow:hidden;background:rgba(8,8,16,0.95);display:flex;flex-direction:column;}
.cards-1 .card{width:35vw;height:80vh;}
.cards-2 .card{width:30vw;height:78vh;}
.cards-3 .card{width:26vw;height:76vh;}
.card-img{flex:1;overflow:hidden;min-height:0;}
.card-img img{width:100%;height:100%;object-fit:cover;}
.card-body{padding:2vh 1.5vw;text-align:center;flex-shrink:0;}
.card-name{font-size:clamp(16px,2.2vmin,26px);font-weight:400;margin-bottom:0.8vh;}
.card-price{font-size:clamp(22px,2.8vmin,34px);font-weight:800;}

/* 이미지 명언 슬라이드 - 풀스크린 + Ken Burns */
.slide-quote-img{background:#000;padding:0;}
.qimg-bg{position:absolute;inset:0;background-size:contain;background-position:center;background-repeat:no-repeat;}
.slide-quote-img.active .qimg-bg{animation:qKenBurns 10s ease-out forwards;}
@keyframes qKenBurns{0%{transform:scale(1);}100%{transform:scale(1.06);}}

/* 명언 슬라이드 - 50:50 + Ken Burns 줌 */
.slide-extra{flex-direction:row;align-items:stretch;}
.extra-left{flex:1;position:relative;overflow:hidden;}
.zoom-wrap{position:absolute;inset:-20px;}
@keyframes kenBurns{
  0%{transform:scale(1);}
  100%{transform:scale(1.18);}
}
.zoom-img{width:100%;height:100%;background-size:cover;background-position:center;}
.slide.active .zoom-img{animation:kenBurns 18s ease-in-out forwards;}
.extra-overlay{position:absolute;inset:0;z-index:2;}
.extra-right{flex:1;display:flex;align-items:center;justify-content:center;padding:80px;z-index:5;}
.extra-content{text-align:center;}

@keyframes fadeUp{from{opacity:0;transform:translateY(30px);}to{opacity:1;transform:translateY(0);}}
.extra-who{font-size:19px;letter-spacing:14px;font-weight:800;border-bottom:2px solid;padding-bottom:12px;display:inline-block;margin-bottom:38px;opacity:0;}
.extra-en{font-family:'Playfair Display';font-size:46px;text-transform:uppercase;line-height:1.2;margin-bottom:32px;opacity:0;}
.extra-ko{font-size:26px;font-weight:300;letter-spacing:2px;opacity:0;}
.slide.active .extra-who{animation:fadeUp 1s ease 0.5s forwards;}
.slide.active .extra-en{animation:fadeUp 1.2s ease 0.9s forwards;}
.slide.active .extra-ko{animation:fadeUp 1.2s ease 1.3s forwards;}

</style>
</head>
<body>
<div class="slideshow" id="ss">''' + "".join(slides) + '''</div>
<script>
const slides=document.querySelectorAll('.slide');
let cur=0, t0=Date.now(), paused=false;
function show(i){
  slides[cur].classList.remove('active');
  cur=(i+slides.length)%slides.length;
  slides[cur].classList.add('active');
  const s=slides[cur];
  document.body.style.background=s.dataset.atmos||'#060609';
  t0=Date.now();
}
function tick(){
  if(!paused){
    const s=slides[cur];
    const fast=s.classList.contains('slide-title')||s.classList.contains('slide-menu');
    const dur=fast?3000:10000;
    const pct=Math.min((Date.now()-t0)/dur*100,100);
    if(pct>=100)show(cur+1);
  }
  requestAnimationFrame(tick);
}
document.addEventListener('keydown',e=>{
  if(e.key==='ArrowRight')show(cur+1);
  else if(e.key==='ArrowLeft')show(cur-1);
  else if(e.key===' '){
      paused = !paused;
      if(!paused) t0 = Date.now();
  }
  else if(e.key==='f'||e.key==='F'){
      if(!document.fullscreenElement) document.documentElement.requestFullscreen();
      else document.exitFullscreen();
  }
});
document.addEventListener('click',()=>show(cur+1));
tick();
</script>
</body>
</html>'''

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    
    total_extra = sum(1 for s in slides if 'slide-extra' in s)
    total_menu  = sum(1 for s in slides if 'slide-menu' in s)
    print(f"v8.0 Build OK | 명언:{total_extra} | 메뉴:{total_menu} | 총:{len(slides)} 슬라이드")

if __name__=="__main__":
    build()
