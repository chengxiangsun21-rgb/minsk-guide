#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
明斯克城市漫游指南 —— 网页生成器（英文版）

作业说明：用 Python 生成一个主题网页（静态 HTML），再发布到免费平台。
运行方式（无需安装任何第三方库，Python 3 自带环境即可）：
    python generate.py
运行后会在同目录生成 index.html，直接用浏览器打开即可查看，
也可以把 index.html 上传到 GitHub Pages 等免费平台发布。

关键词优化（2026-11-19 晚，按老师分享会的要求）：
    先用 Google Trends 查热度，筛选出短尾组（Minsk / Belarus travel /
    Minsk travel / Minsk guide）和长尾组（best places in Minsk /
    things to do in Minsk / Minsk city guide），再自然布置到标题、描述、
    H2 和正文里；全部可见布置，无隐藏文字、无堆砌。详见 keyword-report.md。

访问计数器（2026-11-20，按老师新要求）：
    两个计数器：① 自己写的 JavaScript 计数器（localStorage 记当前浏览器
    的访问次数，显示在页脚）；② Yandex Metrica 计数器（知名 API，
    统计全站访问量）。Metrica 需要自己的计数器编号，见 YANDEX_METRIKA_ID。

实现思路：
    内容（景点 / 美食 / 行程 / 贴士）全部写成 Python 的列表和字典，
    再由 render_* 函数拼成 HTML，最后由 build_page() 组装成完整页面。
    想改内容时只改下面的数据区，不用动 HTML 模板。
"""

import html
from pathlib import Path

# ---------------------------------------------------------------- 网站信息
# 标题标签：就是长尾关键词 Minsk city guide 本身（上周原版标题，今晚任务直接沿用）。
PAGE_TITLE = "Minsk City Guide"
# meta 描述：143 个字符，自然包含长尾词 things to do in Minsk（老师清单里“描述”是关键词布置位置之一）。
META_DESCRIPTION = (
    "Planning a trip to Minsk? Discover the best things to do in Minsk: "
    "Independence Square, the National Library, local food and a 3-day itinerary."
)

# ---------------------------------------------------------------- 计数器
# Yandex Metrica 计数器编号：2026-11-20 在 metrica.yandex.com 创建，
# 计数器名 "Minsk City Guide"，网站地址 chengxiangsun21-rgb.github.io，
# 编号 114398400。换计数器时改这里，重新运行脚本、重新上传 index.html 即可。
YANDEX_METRIKA_ID = "114398400"

# ---------------------------------------------------------------- 数据区
# 页面基本信息（页面内容为英文，页脚保留一行中文城市名作为点缀）
CITY = {
    "name": "Minsk",
    "name_zh": "明斯克",
    "tagline": "The capital of Belarus · A green city on the Svislach River",
    "intro": (
        "Minsk is the capital and largest city of Belarus, home to nearly "
        "two million people on the banks of the Svislach River. Wide Stalinist "
        "avenues, Soviet-era metro stations, post-war memorial squares and old "
        "churches tucked into the lanes of the Upper Town give the city its "
        "unusual character — and make it a natural first stop for Belarus travel. "
        "For most Minsk travel plans, two or three days is enough to see the best of it."
    ),
}

# 城市速览（事实卡片）
FACTS = [
    ("Population", "Around 2 million"),
    ("Currency", "Belarusian Ruble (BYN)"),
    ("Languages", "Russian, Belarusian"),
    ("Metro", "3 lines"),
    ("Best season", "May – September"),
    ("Time zone", "UTC+3"),
]

# 必去景点：英文名 / 当地名 / 标签 / 简介 / 地铁
SIGHTS = [
    {
        "name": "Independence Square & the Red Church",
        "name_local": "Ploshcha Niezalezhnastsi",
        "tag": "City landmark",
        "desc": (
            "One of the largest squares in Europe, flanked by the House of "
            "Government from the early 1930s and the main building of Belarusian "
            "State University. On its western corner stands the Church of Saints "
            "Simon and Helena, built of dark red brick in 1905–1910 — the most "
            "photographed building in Minsk."
        ),
        "metro": "Metro Line 1 · Ploshcha Lenina station",
    },
    {
        "name": "Victory Square",
        "name_local": "Ploshcha Peramohi",
        "tag": "Memorial",
        "desc": (
            "Minsk's main WWII memorial: a tall granite obelisk crowned with the "
            "Order of Victory, an eternal flame burning at its foot, and an "
            "underground hall of memory whose walls carry the names of decorated "
            "soldiers and partisans."
        ),
        "metro": "Metro Line 1 · Ploshcha Peramohi station",
    },
    {
        "name": "Island of Tears",
        "name_local": "Ostrov Slyoz",
        "tag": "Memorial",
        "desc": (
            "A small artificial island in the Svislach, reached by a footbridge "
            "from Trinity Suburb. Its memorial complex honours the Belarusian "
            "soldiers who died in the Soviet–Afghan War of 1979–1989; the weeping "
            "angel statue is the island's most moving sight."
        ),
        "metro": "On foot: footbridge from Trinity Suburb",
    },
    {
        "name": "National Library of Belarus",
        "name_local": "Natsionalnaya Biblioteka",
        "tag": "Architectural wonder",
        "desc": (
            "A glass rhombicuboctahedron opened in 2006, rising more than twenty "
            "storeys high and changing colour after dark — Minsk's most futuristic "
            "landmark. The top-floor observation deck gives a panoramic view over "
            "the whole city."
        ),
        "metro": "Metro Line 1 · Uschod station",
    },
    {
        "name": "Upper Town & Freedom Square",
        "name_local": "Verkhni Gorod",
        "tag": "Old town walk",
        "desc": (
            "The closest Minsk comes to an old town: the medieval market square, "
            "the city hall, and the blue-and-white Holy Spirit Cathedral, part of "
            "a 17th-century monastery. One of the few pockets of pre-war Minsk "
            "still standing — best wandered at dusk."
        ),
        "metro": "Metro Line 2 · Nyamiha station",
    },
    {
        "name": "Minsk Gate",
        "name_local": "Minskaya Brama",
        "tag": "City landmark",
        "desc": (
            "Twin eleven-storey towers in Stalinist Empire style, completed in "
            "1953 to greet every traveller arriving by train. One tower carries "
            "the largest clock in Belarus — many visitors take their first Minsk "
            "photo right here."
        ),
        "metro": "Metro Line 1 · Ploshcha Lenina station",
    },
]

# 必吃美食：名字 / 简介
FOODS = [
    (
        "Draniki (Potato Pancakes)",
        "The national dish: grated potato fried until golden and crisp outside, "
        "soft inside. Always with a spoonful of sour cream.",
    ),
    (
        "Borscht",
        "A deep-red beetroot soup served with sour cream and dark bread — "
        "the warmest thing you can eat on a cold day.",
    ),
    (
        "Kvass",
        "A lightly sweet, slightly fizzy drink fermented from dark bread. "
        "Sold on street corners in summer for a couple of rubles a cup.",
    ),
    (
        "Kolduny (Belarusian Dumplings)",
        "Hearty meat-filled dumplings served with butter and sour cream. "
        "Made for the end of a long day of walking.",
    ),
]

# 三日行程：每天的标题与安排
ITINERARY = [
    (
        "Day 1 · The main axis",
        "Independence Square → the Red Church → a walk down Independence Avenue "
        "→ Victory Square → sunset in Gorky Park",
    ),
    (
        "Day 2 · History & the old town",
        "Museum of the Great Patriotic War → Island of Tears → Trinity Suburb "
        "→ the Upper Town → dinner on Freedom Square",
    ),
    (
        "Day 3 · Views & souvenirs",
        "National Library observation deck → a stroll around the Opera Theatre "
        "→ the central market for souvenirs → draniki at a local restaurant",
    ),
]

# 实用贴士
TIPS = [
    "The metro has 3 lines covering the centre and is cheap; Line 1 runs under "
    "Independence Avenue, which makes it the easiest way to explore the main axis.",
    "The currency is the Belarusian ruble (BYN). Cards are widely accepted in "
    "malls, but keep some cash for small shops and museum tickets.",
    "Plugs are type C / F, 220V — bring an adapter if your devices use a different plug.",
    "May to September is the best time for walking; winters are long and cold, "
    "so dress warmly.",
    "Russian is the everyday language; younger people speak some English. "
    "A couple of Russian phrases for directions go a long way.",
]

# ---------------------------------------------------------------- 样式区
# 纯 CSS，不依赖任何外部图片或字体文件，单文件就能完整显示。
CSS = """
:root {
    --navy: #1e3a5f;
    --navy-light: #2c5282;
    --gold: #e8a33d;
    --ink: #22303c;
    --muted: #66788a;
    --line: #e3e9ef;
    --bg: #f6f8fa;
    --card: #ffffff;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: "Segoe UI", "Helvetica Neue", Arial,
                 "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    color: var(--ink);
    background: var(--bg);
    line-height: 1.7;
}
a { color: var(--navy-light); }
header.hero {
    background: linear-gradient(135deg, #16283f 0%, #1e3a5f 55%, #2c5282 100%);
    color: #fff;
    padding: 72px 20px 56px;
    text-align: center;
}
.hero .kicker { letter-spacing: .35em; font-size: 13px; color: var(--gold); }
.hero h1 { font-size: 44px; margin: 12px 0 8px; letter-spacing: .04em; }
.hero .tagline { font-size: 18px; opacity: .92; }
.hero .intro {
    max-width: 720px; margin: 20px auto 0;
    font-size: 15px; opacity: .85; text-align: left;
}
nav {
    position: sticky; top: 0; z-index: 10;
    background: #fff; border-bottom: 1px solid var(--line);
    display: flex; justify-content: center; gap: 4px; flex-wrap: wrap;
    padding: 10px;
}
nav a {
    text-decoration: none; color: var(--ink); font-size: 14px;
    padding: 6px 14px; border-radius: 999px;
}
nav a:hover { background: #eef3f8; }
main { max-width: 960px; margin: 0 auto; padding: 8px 20px 64px; }
section { padding-top: 44px; }
h2 { font-size: 24px; margin-bottom: 6px; }
.lead { color: var(--muted); font-size: 14px; margin-bottom: 20px; }
.facts {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;
}
.fact {
    background: var(--card); border: 1px solid var(--line); border-radius: 12px;
    padding: 16px; text-align: center;
}
.fact b { display: block; font-size: 18px; color: var(--navy); }
.fact span { font-size: 13px; color: var(--muted); }
.cards {
    display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px;
}
.card {
    background: var(--card); border: 1px solid var(--line); border-radius: 14px;
    padding: 20px; border-top: 4px solid var(--gold);
    display: flex; flex-direction: column; gap: 8px;
}
.card h3 { font-size: 18px; }
.card .local { font-size: 12px; color: var(--muted); font-style: italic; }
.card .tag {
    display: inline-block; font-size: 12px; color: var(--navy-light);
    background: #eaf1f8; border-radius: 999px; padding: 2px 10px; width: fit-content;
}
.card p { font-size: 14px; color: #3d4e5e; flex: 1; }
.card .metro { font-size: 13px; color: var(--muted); }
.star {
    align-self: flex-start; cursor: pointer; border: 1px solid var(--line);
    background: #fff; border-radius: 999px; padding: 4px 12px; font-size: 13px;
}
.star.on { background: #fdf3e0; border-color: var(--gold); }
.food-list { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.food {
    background: var(--card); border: 1px solid var(--line); border-radius: 12px;
    padding: 16px 18px;
}
.food b { color: var(--navy); }
.food p { font-size: 14px; color: #3d4e5e; margin-top: 4px; }
.days { display: flex; flex-direction: column; gap: 12px; }
.day {
    display: flex; gap: 16px; background: var(--card);
    border: 1px solid var(--line); border-radius: 12px; padding: 16px 18px;
}
.day b { white-space: nowrap; color: var(--navy); }
.day span { font-size: 14px; color: #3d4e5e; }
.tips { background: #fff8ec; border: 1px solid #f3e2b8; border-radius: 14px; padding: 20px 24px; }
.tips li { font-size: 14px; margin: 6px 0 6px 18px; }
footer {
    text-align: center; color: var(--muted); font-size: 13px;
    padding: 28px 16px 40px;
}
footer .counter { margin-top: 8px; font-size: 12px; }
@media (max-width: 640px) {
    .hero h1 { font-size: 32px; }
    .facts, .cards, .food-list { grid-template-columns: 1fr; }
    .day { flex-direction: column; gap: 4px; }
}
"""

# 收藏功能：点星标收藏景点，数量实时显示，用 localStorage 记住选择。
JS = """
const stars = document.querySelectorAll('.star');
const counter = document.getElementById('fav-count');
const saved = JSON.parse(localStorage.getItem('minsk-favs') || '[]');
function refresh() {
    const on = document.querySelectorAll('.star.on').length;
    counter.textContent = on > 0
        ? 'Saved ' + on + ' sight' + (on === 1 ? '' : 's')
        : 'Tap the star to save sights you want to visit';
}
stars.forEach(btn => {
    const key = btn.dataset.key;
    if (saved.includes(key)) btn.classList.add('on');
    btn.textContent = btn.classList.contains('on') ? '★ Saved' : '☆ Save';
    btn.addEventListener('click', () => {
        btn.classList.toggle('on');
        btn.textContent = btn.classList.contains('on') ? '★ Saved' : '☆ Save';
        const keys = [...document.querySelectorAll('.star.on')].map(b => b.dataset.key);
        localStorage.setItem('minsk-favs', JSON.stringify(keys));
        refresh();
    });
});
refresh();
"""

# 访问计数器（自己写的 JavaScript 计数器）：每次打开页面，localStorage 里的
# 次数加 1，再显示到页脚。注意：localStorage 只记当前浏览器里的访问次数，
# 换浏览器或清缓存会重新计数；全站总访问量由 Yandex Metrica 计数器统计。
JS_COUNTER = """
(function () {
    var key = 'minsk-guide-visits';
    var visits = parseInt(localStorage.getItem(key) || '0', 10) + 1;
    localStorage.setItem(key, visits);
    var el = document.getElementById('visit-count');
    if (el) {
        el.textContent = visits;
    }
})();
"""

# Yandex Metrica 计数器代码（Yandex 官方标准代码，编号由 YANDEX_METRIKA_ID 填入）。
METRIKA_SNIPPET = """
<!-- Yandex.Metrika counter -->
<script type="text/javascript">
   (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
   m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
   (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
   ym(__METRIKA_ID__, "init", {
        clickmap:true,
        trackLinks:true,
        accurateTrackBounce:true
   });
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/__METRIKA_ID__" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika counter -->
""".replace("__METRIKA_ID__", YANDEX_METRIKA_ID)

# ---------------------------------------------------------------- 渲染区
def esc(text: str) -> str:
    """转义 HTML 特殊字符，避免内容里的 < > & 破坏页面结构。"""
    return html.escape(text)


def render_facts() -> str:
    """城市速览：事实卡片网格。"""
    cards = "".join(
        f'<div class="fact"><b>{esc(value)}</b><span>{esc(label)}</span></div>'
        for label, value in FACTS
    )
    return f'<div class="facts">{cards}</div>'


def render_sights() -> str:
    """必去景点：每处景点一张卡片，带星标收藏按钮。"""
    cards = []
    for i, s in enumerate(SIGHTS):
        cards.append(
            f"""<article class="card">
      <span class="tag">{esc(s["tag"])}</span>
      <h3>{esc(s["name"])}</h3>
      <div class="local">{esc(s["name_local"])}</div>
      <p>{esc(s["desc"])}</p>
      <div class="metro">🚇 {esc(s["metro"])}</div>
      <button class="star" data-key="sight-{i}">☆ Save</button>
    </article>"""
        )
    return '<div class="cards">' + "".join(cards) + "</div>"


def render_foods() -> str:
    """必吃美食：两列小卡片。"""
    items = "".join(
        f'<div class="food"><b>{esc(name)}</b><p>{esc(desc)}</p></div>'
        for name, desc in FOODS
    )
    return f'<div class="food-list">{items}</div>'


def render_itinerary() -> str:
    """三日行程：每天一行。"""
    rows = "".join(
        f'<div class="day"><b>{esc(day)}</b><span>{esc(plan)}</span></div>'
        for day, plan in ITINERARY
    )
    return f'<div class="days">{rows}</div>'


def render_tips() -> str:
    """实用贴士：黄色提示框里的列表。"""
    items = "".join(f"<li>{esc(t)}</li>" for t in TIPS)
    return f'<ul class="tips">{items}</ul>'


def build_page() -> str:
    """组装完整 HTML 页面并返回字符串。"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(PAGE_TITLE)}</title>
<meta name="description" content="{esc(META_DESCRIPTION)}">
{METRIKA_SNIPPET}
<style>{CSS}</style>
</head>
<body>
<header class="hero">
  <div class="kicker">MINSK · BELARUS</div>
  <h1>Minsk City Guide</h1>
  <div class="tagline">{esc(CITY["tagline"])}</div>
  <p class="intro">{esc(CITY["intro"])}</p>
</header>
<nav>
  <a href="#facts">At a glance</a>
  <a href="#sights">Best places</a>
  <a href="#foods">What to eat</a>
  <a href="#plan">3-day plan</a>
  <a href="#tips">Good to know</a>
</nav>
<main>
  <section id="facts">
    <h2>At a Glance</h2>
    <p class="lead">A few numbers to know before you arrive in Minsk.</p>
    {render_facts()}
  </section>
  <section id="sights">
    <h2>Best Places in Minsk</h2>
    <p class="lead">The best things to do in Minsk — grand squares, memorials and one very futuristic library. <span id="fav-count"></span></p>
    {render_sights()}
  </section>
  <section id="foods">
    <h2>What to Eat</h2>
    <p class="lead">Belarusian food is hearty and warming — don't miss these four.</p>
    {render_foods()}
  </section>
  <section id="plan">
    <h2>3-Day Plan</h2>
    <p class="lead">At this pace, three days covers all the highlights — unhurried.</p>
    {render_itinerary()}
  </section>
  <section id="tips">
    <h2>Good to Know</h2>
    <p class="lead">A quick read before you go saves a few wrong turns.</p>
    {render_tips()}
  </section>
</main>
<footer>
  {esc(CITY["name_zh"])} · Minsk City Guide — a short Minsk guide generated by the Python script generate.py.
  Edit the data in the script and run it again to update the page.
  <p class="counter">Visits from this browser: <span id="visit-count">…</span></p>
</footer>
<script>{JS}
{JS_COUNTER}</script>
</body>
</html>
"""


def main() -> None:
    """生成 index.html，放到脚本所在的目录。"""
    base = Path(__file__).resolve().parent
    (base / "index.html").write_text(build_page(), encoding="utf-8")
    print(f"已生成：{base / 'index.html'}")
    print(f"标题 {len(PAGE_TITLE)} 字符 · 描述 {len(META_DESCRIPTION)} 字符")
    print(f"景点 {len(SIGHTS)} 个 · 美食 {len(FOODS)} 种 · 行程 {len(ITINERARY)} 天 · 贴士 {len(TIPS)} 条")


if __name__ == "__main__":
    main()
