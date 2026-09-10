#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Light-themed Academic PDF Presentation Generator
Matches the Swiss minimalist aesthetic of slides_5_6_7_privacy_data_protection.pdf:
- Clean light background (#f7f8fb)
- Spaced category header (І С Т О Р І Я   П Р И В А Т Н О С Т І   Т А   З А Х И С Т У   Д А Н И Х)
- Accent blue number (#2a7e9e) with slate heading (#1e2a35) and muted subtitle (#5b6b79)
- Rounded cards with subtle borders (#d6e0e8) and deep navy featured cards (#16314f)
- Precision typography with LiberationSans
"""

import os
import sys
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

# ------------------------------------------------------------------------------
# 1. Page Geometry & Colors
# ------------------------------------------------------------------------------
WIDTH = 960.0
HEIGHT = 540.0
PAGESIZE = (WIDTH, HEIGHT)

BG_CANVAS = colors.HexColor("#f7f8fb")
TEXT_MAIN = colors.HexColor("#1e2a35")
TEXT_MUTED = colors.HexColor("#5b6b79")
TEXT_SUBTLE = colors.HexColor("#798692")
ACCENT_BLUE = colors.HexColor("#2a7e9e")
ACCENT_NAVY = colors.HexColor("#16314f")
ACCENT_DARK_BLUE = colors.HexColor("#1b4864")
ACCENT_TEAL = colors.HexColor("#0f766e")
CARD_BG_WHITE = colors.HexColor("#ffffff")
CARD_BG_TINT = colors.HexColor("#eef6f8")
CARD_BG_MUTED = colors.HexColor("#eff5f8")
BORDER_CARD = colors.HexColor("#d6e0e8")
BORDER_SUBTLE = colors.HexColor("#e2e8f0")

# ------------------------------------------------------------------------------
# 2. Font Registration
# ------------------------------------------------------------------------------
FONT_REGULAR_PATH = "/usr/share/fonts/liberation-sans-fonts/LiberationSans-Regular.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/liberation-sans-fonts/LiberationSans-Bold.ttf"
FONT_ITALIC_PATH = "/usr/share/fonts/liberation-sans-fonts/LiberationSans-Italic.ttf"

if os.path.exists(FONT_REGULAR_PATH) and os.path.exists(FONT_BOLD_PATH):
    pdfmetrics.registerFont(TTFont("LibSans", FONT_REGULAR_PATH))
    pdfmetrics.registerFont(TTFont("LibSans-Bold", FONT_BOLD_PATH))
    if os.path.exists(FONT_ITALIC_PATH):
        pdfmetrics.registerFont(TTFont("LibSans-Italic", FONT_ITALIC_PATH))
    else:
        pdfmetrics.registerFont(TTFont("LibSans-Italic", FONT_REGULAR_PATH))
else:
    pdfmetrics.registerFont(TTFont("LibSans", "Helvetica"))
    pdfmetrics.registerFont(TTFont("LibSans-Bold", "Helvetica-Bold"))
    pdfmetrics.registerFont(TTFont("LibSans-Italic", "Helvetica-Oblique"))

# ------------------------------------------------------------------------------
# 3. Helper Functions
# ------------------------------------------------------------------------------
def draw_bg(c):
    c.setFillColor(BG_CANVAS)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)

def draw_hdr(c, section_range="01–07"):
    c.setFont("LibSans-Bold", 8.5)
    c.setFillColor(TEXT_MUTED)
    c.drawString(50, 506, "І С Т О Р І Я   П Р И В А Т Н О С Т І   Т А   З А Х И С Т У   Д А Н И Х")
    c.drawRightString(910, 506, section_range)

def draw_title_bar(c, num_str, title_str, subtitle_str):
    c.setFont("LibSans-Bold", 24)
    c.setFillColor(ACCENT_BLUE)
    c.drawString(50, 458, num_str)
    
    num_w = c.stringWidth(num_str + " ", "LibSans-Bold", 24)
    c.setFont("LibSans-Bold", 22)
    c.setFillColor(TEXT_MAIN)
    c.drawString(50 + num_w, 458, title_str)
    
    c.setFont("LibSans", 11)
    c.setFillColor(TEXT_MUTED)
    c.drawString(50 + num_w, 435, subtitle_str)

def draw_ftr(c, sources_text, page_num_str):
    c.setFont("LibSans", 7.2)
    c.setFillColor(TEXT_SUBTLE)
    c.drawString(50, 18, f"Джерела: {sources_text}")
    c.drawRightString(910, 18, page_num_str)

def card(c, x, y, w, h, bg=CARD_BG_WHITE, border=BORDER_CARD, rx=8):
    c.setFillColor(bg)
    if border:
        c.setStrokeColor(border)
        c.setLineWidth(1)
        c.roundRect(x, y, w, h, rx, fill=1, stroke=1)
    else:
        c.roundRect(x, y, w, h, rx, fill=1, stroke=0)

def pill(c, x, y, text, bg=ACCENT_BLUE, text_color=colors.white, font_size=8, h=20, rx=4, pad_x=8):
    c.setFont("LibSans-Bold", font_size)
    tw = c.stringWidth(text, "LibSans-Bold", font_size)
    pw = tw + pad_x * 2
    c.setFillColor(bg)
    c.roundRect(x, y, pw, h, rx, fill=1, stroke=0)
    c.setFillColor(text_color)
    c.drawCentredString(x + pw / 2, y + (h - font_size) / 2 + 1, text)
    return pw

def p_box(c, html_text, x, y, w, font="LibSans", size=9.5, color=TEXT_MAIN, leading=13, align="left"):
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
    align_map = {"left": TA_LEFT, "center": TA_CENTER, "right": TA_RIGHT, "justify": TA_JUSTIFY}
    style = ParagraphStyle(
        name=f"p_{x}_{y}_{size}",
        fontName=font,
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=align_map.get(align, TA_LEFT)
    )
    p = Paragraph(html_text, style)
    rw, rh = p.wrap(w, HEIGHT)
    p.drawOn(c, x, y - rh)
    return rh

## ------------------------------------------------------------------------------
# SLIDE 1: Title Slide (Simple & Clean Minimalist)
# ------------------------------------------------------------------------------
def render_slide_1(c, page_num=1, total_pages=7):
    draw_bg(c)
    draw_hdr(c, f"01–{total_pages:02d}")
    draw_ftr(c, "Міжнародно-правові акти Ради Європи, Європейського Союзу та судова практика ЄСПЛ.", str(page_num))
    
    # Big Clean Title
    c.setFont("LibSans-Bold", 26)
    c.setFillColor(ACCENT_BLUE)
    c.drawString(50, 460, "01")
    
    num_w = c.stringWidth("01  ", "LibSans-Bold", 26)
    c.setFont("LibSans-Bold", 23)
    c.setFillColor(TEXT_MAIN)
    c.drawString(50 + num_w, 460, "Історія міжнародно-правового становлення права на приватність")
    
    c.setFont("LibSans", 11.5)
    c.setFillColor(TEXT_MUTED)
    c.drawString(50 + num_w, 436, "Від концепції «права бути залишеним у спокої» до сучасних стандартів захисту персональних даних")
    
    # Subtle horizontal line
    c.setStrokeColor(BORDER_SUBTLE)
    c.setLineWidth(1)
    c.line(50, 416, 910, 416)
    
    # Section: Доповідачі (3 clean balanced cards)
    c.setFont("LibSans-Bold", 10)
    c.setFillColor(ACCENT_DARK_BLUE)
    c.drawString(50, 394, "ДОПОВІДАЧІ:")
    
    presenters = [
        ("Присяжний Савелій", "Група ІМ-55"),
        ("Пашко Ростислав", "Група ІП-53"),
        ("Олександр Тузюк", "Група ІО-53")
    ]
    
    card_w = 273
    card_h = 136
    card_y = 238
    gap = 20
    
    for i, (name, group) in enumerate(presenters):
        cx = 50 + i * (card_w + gap)
        # White card with subtle border
        card(c, cx, card_y, card_w, card_h, bg=CARD_BG_WHITE, border=BORDER_CARD, rx=8)
        
        # Pill badge
        pill(c, cx + 20, card_y + card_h - 32, "ДОПОВІДАЧ",
             bg=CARD_BG_TINT, text_color=ACCENT_DARK_BLUE, font_size=8, h=20, rx=4, pad_x=10)
        
        # Presenter Name
        c.setFont("LibSans-Bold", 17)
        c.setFillColor(TEXT_MAIN)
        c.drawString(cx + 20, card_y + card_h - 66, name)
        
        # Inner divider line
        c.setStrokeColor(BORDER_SUBTLE)
        c.setLineWidth(1)
        c.line(cx + 20, card_y + card_h - 82, cx + card_w - 20, card_y + card_h - 82)
        
        # Academic Group
        c.setFont("LibSans-Bold", 12.5)
        c.setFillColor(ACCENT_BLUE)
        c.drawString(cx + 20, card_y + card_h - 106, group)
        
        c.setFont("LibSans", 9)
        c.setFillColor(TEXT_MUTED)
        c.drawString(cx + 20, card_y + card_h - 123, "Студент-дослідник")
    
    # Bottom: 3-step Presentation Roadmap Card
    bot_y = 54
    bot_h = 154
    card(c, 50, bot_y, 860, bot_h, bg=CARD_BG_WHITE, border=BORDER_CARD, rx=8)
    
    c.setFont("LibSans-Bold", 10)
    c.setFillColor(ACCENT_DARK_BLUE)
    c.drawString(72, bot_y + bot_h - 26, "СТРУКТУРА ДОПОВІДІ (3 КЛЮЧОВІ ЕТАПИ):")
    
    col_w = 250
    col_x_list = [72, 362, 652]
    
    stages = [
        ("1. ВИТОКИ ТА ДОКТРИНА",
         "• 1890 р. — стаття Воррена і Брандейса<br/>"
         "• Формула «The Right to be Let Alone»<br/>"
         "• Розмежування: Privacy ≠ Data Protection"),
        ("2. МІЖНАРОДНЕ ЗАКРІПЛЕННЯ",
         "• 1948 р. — ст. 12 ЗДПЛ ООН<br/>"
         "• 1950 р. — ст. 8 ЄКПЛ (механізм ЄСПЛ)<br/>"
         "• 1981 р. — Конвенція № 108 Ради Європи"),
        ("3. СТАНДАРТИ ЄС ТА ЦИФРА",
         "• 2000 р. — ст. 7 і 8 Хартії основних прав ЄС<br/>"
         "• 2016 р. — Загальний регламент GDPR<br/>"
         "• Новітні регламенти ЄС: DSA та реклама")
    ]
    
    for idx, (badge, desc) in enumerate(stages):
        col_x = col_x_list[idx]
        
        pill(c, col_x, bot_y + bot_h - 58, badge,
             bg=CARD_BG_TINT, text_color=ACCENT_DARK_BLUE, font_size=8, h=20, rx=4, pad_x=10)
        
        p_box(c, desc, col_x, bot_y + bot_h - 70, col_w,
              size=9.5, color=TEXT_MAIN, leading=15)
    
    c.showPage()

# ------------------------------------------------------------------------------
# SLIDE 2: Privacy vs Data Protection (Airy & Contrasting)
# ------------------------------------------------------------------------------
def render_slide_2(c, page_num=2, total_pages=7):
    draw_bg(c)
    draw_hdr(c, f"01–{total_pages:02d}")
    draw_ftr(c, "ст. 2 ЗУ «Про захист персональних даних»; ст. 4 GDPR; ст. 7–8 Хартії основних прав ЄС.", str(page_num))
    draw_title_bar(c, "02", "Право на приватність ≠ Захист персональних даних",
                   "Чому приватність ширша за конфіденційність, а захист даних є самостійним позитивним правом")
    
    card_y = 95
    card_h = 320
    card_w = 420
    
    # ---------------- LEFT CARD: PRIVACY ----------------
    card(c, 50, card_y, card_w, card_h, bg=CARD_BG_WHITE, border=BORDER_CARD, rx=8)
    
    c.setFont("LibSans-Bold", 14)
    c.setFillColor(TEXT_MAIN)
    c.drawString(70, card_y + card_h - 32, "1. Право на приватність (Privacy)")
    pill(c, 50 + card_w - 120, card_y + card_h - 36, "НЕГАТИВНЕ ПРАВО",
         bg=CARD_BG_TINT, text_color=ACCENT_BLUE, font_size=7.5, h=20, rx=4, pad_x=8)
    
    # Big Concept Box
    card(c, 68, card_y + card_h - 96, card_w - 36, 52, bg=CARD_BG_TINT, border=BORDER_CARD, rx=6)
    c.setFont("LibSans-Bold", 10)
    c.setFillColor(ACCENT_DARK_BLUE)
    c.drawString(80, card_y + card_h - 60, "«The right to be let alone»")
    c.setFont("LibSans", 8.8)
    c.setFillColor(TEXT_MUTED)
    c.drawString(80, card_y + card_h - 76, "Право бути залишеним у спокої • Захист особистого простору людини")
    c.drawString(80, card_y + card_h - 88, "Суб'єктивне право вирішувати, що і коли про себе розкривати іншим.")
    
    # 4 Components
    c.setFont("LibSans-Bold", 9.5)
    c.setFillColor(ACCENT_BLUE)
    c.drawString(70, card_y + 195, "4 ключові складові приватності:")
    
    comp_items = [
        ("Усамітнення (solitude)", "відсутність несанкціонованого нагляду та стеження"),
        ("Анонімність (anonymity)", "можливість діяти публічно без розкриття імені"),
        ("Інтимність (intimacy)", "право на довірче спілкування у вузькому колі близьких"),
        ("Таємниця (reserve)", "самостійний контроль за розголошенням таємниць")
    ]
    for idx, (label, desc) in enumerate(comp_items):
        cy = card_y + 172 - idx * 24
        c.setFillColor(ACCENT_BLUE)
        c.circle(76, cy + 4, 3, fill=1, stroke=0)
        c.setFont("LibSans-Bold", 9)
        c.setFillColor(TEXT_MAIN)
        c.drawString(86, cy, label + " —")
        lw = c.stringWidth(label + " — ", "LibSans-Bold", 9)
        c.setFont("LibSans", 8.5)
        c.setFillColor(TEXT_MUTED)
        c.drawString(86 + lw, cy, desc)
    
    # 4 Spheres Pill
    card(c, 68, card_y + 42, card_w - 36, 32, bg=CARD_BG_MUTED, border=BORDER_SUBTLE, rx=5)
    c.setFont("LibSans-Bold", 8.5)
    c.setFillColor(TEXT_MAIN)
    c.drawString(78, card_y + 53, "Сфери захисту:")
    c.setFont("LibSans", 8.5)
    c.setFillColor(TEXT_MUTED)
    c.drawString(155, card_y + 53, "тілесна • територіальна • комунікаційна • інформаційна")
    
    # Bottom Anchor
    c.setFont("LibSans-Bold", 7.8)
    c.setFillColor(ACCENT_DARK_BLUE)
    c.drawCentredString(50 + card_w / 2, card_y + 18, "Нормативні якорі: ст. 12 ЗДПЛ 1948 • ст. 8 ЄКПЛ 1950 • ст. 7 Хартії ЄС")
    
    # ---------------- RIGHT CARD: DATA PROTECTION (Navy) ----------------
    rx_x = 490
    card(c, rx_x, card_y, card_w, card_h, bg=ACCENT_NAVY, border=None, rx=8)
    
    c.setFont("LibSans-Bold", 14)
    c.setFillColor(colors.white)
    c.drawString(rx_x + 20, card_y + card_h - 32, "2. Захист даних (Data Protection)")
    pill(c, rx_x + card_w - 120, card_y + card_h - 36, "ПОЗИТИВНЕ ПРАВО",
         bg=ACCENT_BLUE, text_color=colors.white, font_size=7.5, h=20, rx=4, pad_x=8)
    
    # Big Concept Box
    card(c, rx_x + 18, card_y + card_h - 96, card_w - 36, 52, bg=colors.HexColor("#20415f"), border=colors.HexColor("#30516d"), rx=6)
    c.setFont("LibSans-Bold", 10)
    c.setFillColor(colors.HexColor("#7ed1e6"))
    c.drawString(rx_x + 30, card_y + card_h - 60, "Контроль за обігом інформації")
    c.setFont("LibSans", 8.8)
    c.setFillColor(colors.HexColor("#e2e8f0"))
    c.drawString(rx_x + 30, card_y + card_h - 76, "ст. 2 ЗУ «Про захист ПД» • ст. 4(1) Регламенту GDPR 2016/679")
    c.drawString(rx_x + 30, card_y + card_h - 88, "Обов'язок володільців даних діяти за чіткими юридичними правилами.")
    
    # 3 Pillars
    c.setFont("LibSans-Bold", 9.5)
    c.setFillColor(colors.HexColor("#7ed1e6"))
    c.drawString(rx_x + 20, card_y + 195, "3 ключові нормативні вимоги:")
    
    dp_boxes = [
        ("01", "Законність та мета", "обробка виключно за наявності згоди або прямої норми закону"),
        ("02", "Права суб'єкта даних", "доступ, виправлення помилок та право на видалення («забуття»)"),
        ("03", "Інституційний нагляд", "обов'язковий контроль незалежного наглядового органу (DPA)")
    ]
    for idx, (num, tit, desc) in enumerate(dp_boxes):
        by = card_y + 140 - idx * 38
        card(c, rx_x + 18, by, card_w - 36, 32, bg=colors.HexColor("#1b3b5c"), border=colors.HexColor("#2a7e9e"), rx=5)
        c.setFont("LibSans-Bold", 9)
        c.setFillColor(colors.HexColor("#7ed1e6"))
        c.drawString(rx_x + 28, by + 19, f"{num}  {tit} —")
        tw = c.stringWidth(f"{num}  {tit} — ", "LibSans-Bold", 9)
        c.setFont("LibSans", 8.2)
        c.setFillColor(colors.HexColor("#e2e8f0"))
        c.drawString(rx_x + 28 + tw, by + 19, desc)
    
    # Bottom Distinction Callout
    card(c, rx_x + 18, card_y + 12, card_w - 36, 50, bg=colors.HexColor("#162a42"), border=colors.HexColor("#23486c"), rx=5)
    p_box(c, "<b>Приватність ≠ Конфіденційність:</b> Публікація фото у соцмережах є реалізацією приватності, а захист даних гарантує законність їх подальшої обробки алгоритмами.",
          rx_x + 26, card_y + 50, card_w - 52, size=8.2, color=colors.HexColor("#e2e8f0"), leading=11.5)
    
    # Bottom summary punchline
    card(c, 50, 42, 860, 40, bg=CARD_BG_TINT, border=BORDER_CARD, rx=6)
    p_box(c, "<b>Головна відмінність:</b> Приватність вимагає не втручатися в особистий простір («залиште мене у спокої»). Захист даних вступає в дію, коли відомості вже зібрані — він регламентує правила їх обігу та запобігає дискримінації.",
          65, 72, 830, size=9, color=ACCENT_DARK_BLUE, leading=13)

    c.showPage()

# ------------------------------------------------------------------------------
# SLIDE 3: Warren & Brandeis 1890 (Clean & Spacious)
# ------------------------------------------------------------------------------
def render_slide_3(c, page_num=3, total_pages=7):
    draw_bg(c)
    draw_hdr(c, f"01–{total_pages:02d}")
    draw_ftr(c, "Warren S., Brandeis L. The Right to Privacy // Harvard Law Review. 1890. Vol. 4, No. 5; Cooley T. Law of Torts. 1879.", str(page_num))
    draw_title_bar(c, "03", "Доктринальні витоки: стаття Воррена і Брандейса",
                   "1890: як винахід компактної камери Kodak Джорджа Істмена спричинив народження концепції приватності")
    
    col_y = 45
    left_w = 260
    right_w = 580
    
    # ---------------- LEFT COLUMN: PORTRAIT ----------------
    card(c, 50, col_y, left_w, 375, bg=CARD_BG_WHITE, border=BORDER_CARD, rx=8)
    
    brandeis_img = "slide-03/louis_brandeis_1915.jpg"
    if os.path.exists(brandeis_img):
        c.drawImage(brandeis_img, 70, col_y + 195, width=220, height=165, preserveAspectRatio=True, mask='auto')
    
    c.setFont("LibSans-Bold", 12.5)
    c.setFillColor(TEXT_MAIN)
    c.drawString(68, col_y + 175, "Луїс Д. Брандейс (1856–1941)")
    
    c.setFont("LibSans-Italic", 9)
    c.setFillColor(ACCENT_BLUE)
    c.drawString(68, col_y + 160, "Співавтор статті, суддя Верховного Суду США")
    
    card(c, 62, col_y + 16, left_w - 24, 135, bg=CARD_BG_TINT, border=BORDER_CARD, rx=6)
    p_box(c, "<b>Публікація:</b> <i>«The Right to Privacy»</i><br/>"
             "<b>Видання:</b> Harvard Law Review, Vol. 4, No. 5<br/>"
             "<b>Дата:</b> 15 грудня 1890 р.<br/><br/>"
             "<b>Співавтор:</b> Семюель Д. Воррен (бостонський юрист, випускник Гарварду).<br/><br/>"
             "<i>Найбільш цитована наукова стаття в історії права.</i>",
          70, col_y + 140, left_w - 40, size=8.8, color=TEXT_MAIN, leading=13)
    
    # ---------------- RIGHT COLUMN: 3 CRISP CARDS ----------------
    rx_x = 330
    card_h = 115
    gap = 15
    
    # Card 1: Kodak & Yellow Press
    c1_y = col_y + 2 * (card_h + gap)
    card(c, rx_x, c1_y, right_w, card_h, bg=CARD_BG_WHITE, border=BORDER_CARD, rx=8)
    pill(c, rx_x + 18, c1_y + card_h - 28, "1888 • ТЕХНОЛОГІЧНИЙ ТРИГЕР",
         bg=ACCENT_BLUE, text_color=colors.white, font_size=8, h=20, rx=4, pad_x=10)
    c.setFont("LibSans-Bold", 12)
    c.setFillColor(TEXT_MAIN)
    c.drawString(rx_x + 185, c1_y + card_h - 24, "Камера Kodak та поява таблоїдів")
    
    p_box(c, "• <b>Поява камери Kodak (1888):</b> Джордж Істмен запатентував першу портативну ручну камеру з рулонною плівкою під гаслом <i>«You press the button, we do the rest»</i>. Знімати людину стало можливим миттєво і без її відома.<br/>"
             "• <b>Сенсаційна преса:</b> Бостонські газети почали масово публікувати плітки та фото про приватне життя. Старе право захищало лише паркан (делікт <i>trespass</i>) чи речі, але не право на спокій.",
          rx_x + 18, c1_y + card_h - 40, right_w - 36, size=9.2, color=TEXT_MAIN, leading=14)
    
    # Card 2: The Right to be Let Alone
    c2_y = col_y + card_h + gap
    card(c, rx_x, c2_y, right_w, card_h, bg=CARD_BG_WHITE, border=BORDER_CARD, rx=8)
    pill(c, rx_x + 18, c2_y + card_h - 28, "1879 • ТОМАС КУЛІ",
         bg=ACCENT_DARK_BLUE, text_color=colors.white, font_size=8, h=20, rx=4, pad_x=10)
    c.setFont("LibSans-Bold", 12)
    c.setFillColor(TEXT_MAIN)
    c.drawString(rx_x + 140, c2_y + card_h - 24, "Концепція «The Right to be Let Alone»")
    
    p_box(c, "• <b>Формула судді Томаса Кулі:</b> Запозичено з трактату <i>«A Treatise on the Law of Torts»</i> (1879 р.): <i>«The right to one's person may be said to be a right of complete immunity: to be let alone»</i>.<br/>"
             "• <b>Доктринальний прорив:</b> Воррен і Брандейс довели, що приватне життя має самостійну правову цінність, а публічне втручання в особистий простір є <b>цивільним правопорушенням</b> із правом на компенсацію моральної шкоди.",
          rx_x + 18, c2_y + card_h - 40, right_w - 36, size=9.2, color=TEXT_MAIN, leading=14)
    
    # Card 3: Paradigm Shift (Tinted)
    c3_y = col_y
    card(c, rx_x, c3_y, right_w, card_h, bg=CARD_BG_TINT, border=BORDER_CARD, rx=8)
    pill(c, rx_x + 18, c3_y + card_h - 28, "ПАРАДИГМАЛЬНИЙ ЗСУВ",
         bg=ACCENT_TEAL, text_color=colors.white, font_size=8, h=20, rx=4, pad_x=10)
    c.setFont("LibSans-Bold", 12)
    c.setFillColor(ACCENT_DARK_BLUE)
    c.drawString(rx_x + 160, c3_y + card_h - 24, "Від захисту майна — до захисту особи")
    
    p_box(c, "• <b>Еволюція:</b> тілесне життя → речова власність і земля → інтелектуальна власність → <b>духовна недоторканність особистості <i>(inviolate personality)</i></b>.<br/>"
             "• <b>Історичний міст:</b> Саме ця стаття заклала ідейний фундамент, з якого у 1948 році виросла стаття 12 Загальної декларації прав людини ООН та сучасне європейське законодавство про приватність.",
          rx_x + 18, c3_y + card_h - 40, right_w - 36, size=9.2, color=TEXT_MAIN, leading=14)

    c.showPage()

# ------------------------------------------------------------------------------
# SLIDE 4: UDHR 1948 & ECHR 1950 (Airy 3 Columns)
# ------------------------------------------------------------------------------
def render_slide_4(c, page_num=4, total_pages=7):
    draw_bg(c)
    draw_hdr(c, f"01–{total_pages:02d}")
    draw_ftr(c, "ст. 12 ЗДПЛ ООН 1948; ст. 8 Конвенції Ради Європи 1950; прецеденти ЄСПЛ: Leander (1987), Amann (2000), Rotaru (2000).", str(page_num))
    draw_title_bar(c, "04", "Перші міжнародні акти: ЗДПЛ 1948 та Конвенція Ради Європи 1950",
                   "Перше закріплення (ст. 12 ЗДПЛ), трискладовий тест (ст. 8 ЄКПЛ) та судова практика ЄСПЛ")
    
    col_y = 45
    col_w = 273
    col_h = 375
    gap = 20
    
    # ---------------- COL 1: UDHR 1948 ----------------
    c1_x = 50
    card(c, c1_x, col_y, col_w, col_h, bg=CARD_BG_WHITE, border=BORDER_CARD, rx=8)
    pill(c, c1_x + 14, col_y + col_h - 28, "ООН • 1948",
         bg=ACCENT_BLUE, text_color=colors.white, font_size=8, h=20, rx=4, pad_x=10)
    c.setFont("LibSans-Bold", 11)
    c.setFillColor(TEXT_MAIN)
    c.drawString(c1_x + 95, col_y + col_h - 24, "1. Універсальний акт")
    
    eleanor_img = "slide-04/eleanor_roosevelt_udhr_opt.jpg"
    if os.path.exists(eleanor_img):
        c.drawImage(eleanor_img, c1_x + 15, col_y + col_h - 150, width=col_w - 30, height=115, preserveAspectRatio=True, mask='auto')
    
    c.setFont("LibSans-Bold", 9)
    c.setFillColor(ACCENT_BLUE)
    c.drawString(c1_x + 15, col_y + col_h - 165, "Загальна декларація прав людини")
    c.setFont("LibSans", 7.8)
    c.setFillColor(TEXT_MUTED)
    c.drawString(c1_x + 15, col_y + col_h - 177, "10 грудня 1948 р., Париж")
    
    # Art 12 Box
    card(c, c1_x + 12, col_y + 14, col_w - 24, 175, bg=CARD_BG_TINT, border=BORDER_CARD, rx=6)
    p_box(c, "<b>Стаття 12 ЗДПЛ:</b><br/>"
             "<i>«Ніхто не може зазнавати безпідставного втручання в його особисте і сімейне життя, безпідставного посягання на недоторканність його житла, таємницю його кореспонденції або на його честь і репутацію...»</i><br/><br/>"
             "• <b>Контекст:</b> цивілізаційна відповідь на свавілля Другої світової війни.<br/>"
             "• <b>Значення:</b> перший загальновизнаний глобальний стандарт прав людини.",
          c1_x + 20, col_y + 178, col_w - 40, size=8.5, color=TEXT_MAIN, leading=12.5)
    
    # ---------------- COL 2: ECHR 1950 & 3-PART TEST ----------------
    c2_x = c1_x + col_w + gap
    card(c, c2_x, col_y, col_w, col_h, bg=CARD_BG_WHITE, border=BORDER_CARD, rx=8)
    pill(c, c2_x + 14, col_y + col_h - 28, "РАДА ЄВРОПИ • 1950",
         bg=ACCENT_DARK_BLUE, text_color=colors.white, font_size=8, h=20, rx=4, pad_x=10)
    c.setFont("LibSans-Bold", 11)
    c.setFillColor(TEXT_MAIN)
    c.drawString(c2_x + 135, col_y + col_h - 24, "2. ЄКПЛ: стаття 8")
    
    p_box(c, "<b>Конвенція 1950 р. (ЄКПЛ):</b> перший <b>юридично обов'язковий</b> договір із механізмом судового захисту (ЄСПЛ).<br/><br/>"
             "<b>Трискладовий тест правомірності втручання (ч. 2 ст. 8):</b><br/>"
             "Держава має право на обмеження виключно за 3 критеріїв одночасно:",
          c2_x + 15, col_y + col_h - 40, col_w - 30, size=8.8, color=TEXT_MAIN, leading=13)
    
    # 3 Steps boxes
    steps = [
        ("01", "Згідно із законом", "доступність, чіткість і передбачуваність норми"),
        ("02", "Легітимна мета", "безпека держави, суспільний порядок, права інших"),
        ("03", "Необхідно в суспільстві", "нагальна потреба та пропорційність заходу")
    ]
    for idx, (num, st_title, st_desc) in enumerate(steps):
        sy = col_y + 135 - idx * 52
        card(c, c2_x + 12, sy, col_w - 24, 45, bg=CARD_BG_TINT, border=BORDER_CARD, rx=5)
        c.setFont("LibSans-Bold", 9)
        c.setFillColor(ACCENT_BLUE)
        c.drawString(c2_x + 22, sy + 30, f"{num}  {st_title}")
        c.setFont("LibSans", 8)
        c.setFillColor(TEXT_MUTED)
        c.drawString(c2_x + 22, sy + 14, st_desc)
    
    # Bottom Note
    card(c, c2_x + 12, col_y + 14, col_w - 24, 26, bg=CARD_BG_MUTED, border=BORDER_SUBTLE, rx=4)
    c.setFont("LibSans-Bold", 8)
    c.setFillColor(ACCENT_DARK_BLUE)
    c.drawCentredString(c2_x + col_w / 2, col_y + 22, "Також закріплено: ст. 17 МПГПП ООН 1966 р.")
    
    # ---------------- COL 3: ECTHR PRECEDENTS (Navy) ----------------
    c3_x = c2_x + col_w + gap
    card(c, c3_x, col_y, col_w, col_h, bg=ACCENT_NAVY, border=None, rx=8)
    pill(c, c3_x + 14, col_y + col_h - 28, "ЄСПЛ • PRECEDENTS",
         bg=ACCENT_BLUE, text_color=colors.white, font_size=8, h=20, rx=4, pad_x=10)
    c.setFont("LibSans-Bold", 11)
    c.setFillColor(colors.white)
    c.drawString(c3_x + 130, col_y + col_h - 24, "3. Судова практика")
    
    p_box(c, "ЄСПЛ розглядає Конвенцію як <b>«живий інструмент»</b> <i>(living instrument)</i>, що поширив гарантії ст. 8 на сферу баз даних:",
          c3_x + 15, col_y + col_h - 40, col_w - 30, size=8.8, color=colors.HexColor("#e2e8f0"), leading=12.5)
    
    cases = [
        ("Leander v. Sweden (1987)",
         "<b>Таємні картотеки безпеки:</b><br/>"
         "Збереження відомостей про особу в таємних реєстрах безпеки є <b>втручанням у ст. 8 ЄКПЛ</b>."),
        
        ("Amann v. Switzerland (2000)",
         "<b>Вихід за межі «усамітнення»:</b><br/>"
         "Приватність не обмежується вузьким колом, а охоплює <b>ділову та професійну</b> діяльність."),
        
        ("Rotaru v. Romania (2000)",
         "<b>Досьє спецслужб з відкритих даних:</b><br/>"
         "Систематизація навіть публічних даних є порушенням ст. 8 без права доступу та спростування.")
    ]
    
    for idx, (c_title, c_text) in enumerate(cases):
        cy = col_y + 195 - idx * 92
        card(c, c3_x + 12, cy, col_w - 24, 84, bg=colors.HexColor("#20415f"), border=colors.HexColor("#30516d"), rx=6)
        c.setFont("LibSans-Bold", 9)
        c.setFillColor(colors.HexColor("#7ed1e6"))
        c.drawString(c3_x + 22, cy + 68, c_title)
        p_box(c, c_text, c3_x + 22, cy + 62, col_w - 44, size=8.2, color=colors.HexColor("#e2e8f0"), leading=11.5)

    c.showPage()

# ------------------------------------------------------------------------------
# SLIDE 5: Computerization & Convention 108
# ------------------------------------------------------------------------------
def render_slide_5(c, page_num=5, total_pages=7):
    draw_bg(c)
    draw_hdr(c, f"01–{total_pages:02d}")
    draw_ftr(c, "Council of Europe — Convention 108 / CETS 223; European Parliament Research Service.", str(page_num))
    draw_title_bar(c, f"{page_num:02d}", "Комп’ютеризація та народження «захисту даних»",
                   "1970–1981: від перших електронних баз до міжнародного договору")
    
    # 4 Nodes Timeline across middle
    t_y = 220
    c.setStrokeColor(colors.HexColor("#a9bac6"))
    c.setLineWidth(1.5)
    c.line(110, t_y + 60, 850, t_y + 60)
    
    t_nodes = [
        (110, "1970", "Гессен (ФРН)", "Перший закон про захист\nперсональних даних на рівні землі.", False),
        (330, "1973", "Швеція — Datalagen", "Перший у світі національний закон\nпро захист даних.", False),
        (550, "1981", "Конвенція №108", "Перший юридично обов’язковий\nміжнародний договір у сфері захисту даних.", True),
        (770, "2018", "Конвенція 108+", "Протокол модернізації: цифрові\nризики, посилені права та відповідальність.", False)
    ]
    
    for cx, yr, tit, desc, is_highlight in t_nodes:
        # Node circle
        c.setFillColor(ACCENT_NAVY if is_highlight else CARD_BG_WHITE)
        c.setStrokeColor(ACCENT_NAVY if is_highlight else ACCENT_DARK_BLUE)
        c.setLineWidth(2.5)
        c.circle(cx, t_y + 60, 28, fill=1, stroke=1)
        
        c.setFont("LibSans-Bold", 12)
        c.setFillColor(colors.white if is_highlight else ACCENT_DARK_BLUE)
        c.drawCentredString(cx, t_y + 55, yr)
        
        # Title
        c.setFont("LibSans-Bold", 10.5)
        c.setFillColor(TEXT_MAIN)
        c.drawCentredString(cx, t_y + 12, tit)
        
        # Desc
        lines = desc.split("\n")
        c.setFont("LibSans", 8.5)
        c.setFillColor(TEXT_MUTED)
        for l_idx, line in enumerate(lines):
            c.drawCentredString(cx, t_y - 6 - l_idx * 12, line)
    
    # Bottom Card: Convention 108 Principles
    b_y = 80
    b_h = 100
    card(c, 70, b_y, 820, b_h, bg=CARD_BG_TINT, border=BORDER_CARD, rx=8)
    
    c.setFont("LibSans-Bold", 12)
    c.setFillColor(TEXT_MAIN)
    c.drawString(90, b_y + 58, "Що закріпила Конвенція №108")
    
    pills = [
        ("Законність", ACCENT_BLUE),
        ("Визначена мета", ACCENT_BLUE),
        ("Права особи", ACCENT_BLUE),
        ("Безпека даних", ACCENT_BLUE),
        ("Транскордонні потоки", ACCENT_NAVY)
    ]
    
    px = 310
    for p_text, p_color in pills:
        pw = pill(c, px, b_y + 50, p_text, bg=p_color, text_color=colors.white, font_size=9, h=26, rx=6, pad_x=12)
        px += pw + 12
    
    c.setFont("LibSans", 9)
    c.setFillColor(TEXT_MUTED)
    c.drawString(90, b_y + 22, "108+ ухвалено у 2018 р. як протокол модернізації; станом на вересень 2026 р. він ще очікує набрання чинності.")

    c.showPage()

# ------------------------------------------------------------------------------
# SLIDE 6: EU Standards: Charter & GDPR
# ------------------------------------------------------------------------------
def render_slide_6(c, page_num=6, total_pages=7):
    draw_bg(c)
    draw_hdr(c, f"01–{total_pages:02d}")
    draw_ftr(c, "EUR-Lex — Directive 95/46/EC, Charter of Fundamental Rights (Arts. 7–8), Regulation (EU) 2016/679.", str(page_num))
    draw_title_bar(c, f"{page_num:02d}", "Стандарти ЄС: Хартія та GDPR",
                   "Від гармонізації правил до самостійного фундаментального права")
    
    card_y = 65
    card_h = 340
    left_w = 290
    right_w = 525
    
    # ---------------- LEFT CARD: Directive & Charter ----------------
    card(c, 60, card_y, left_w, card_h, bg=CARD_BG_WHITE, border=BORDER_CARD, rx=8)
    
    # 1995 Directive
    pill(c, 80, card_y + card_h - 40, "1995", bg=ACCENT_NAVY, text_color=colors.white, font_size=10, h=24, rx=6, pad_x=18)
    c.setFont("LibSans-Bold", 12)
    c.setFillColor(TEXT_MAIN)
    c.drawString(185, card_y + card_h - 26, "Директива")
    c.drawString(185, card_y + card_h - 40, "95/46/ЄС")
    
    p_box(c, "Гармонізувала національні правила та стала базовим стандартом ЄС до GDPR.",
          80, card_y + card_h - 58, left_w - 40, size=9, color=TEXT_MUTED, leading=13)
    
    c.setStrokeColor(BORDER_SUBTLE)
    c.setLineWidth(1)
    c.line(90, card_y + card_h - 110, 60 + left_w - 30, card_y + card_h - 110)
    
    # 2000 Charter
    pill(c, 80, card_y + card_h - 150, "2000", bg=ACCENT_BLUE, text_color=colors.white, font_size=10, h=24, rx=6, pad_x=18)
    c.setFont("LibSans-Bold", 12)
    c.setFillColor(TEXT_MAIN)
    c.drawString(185, card_y + card_h - 136, "Хартія основних")
    c.drawString(185, card_y + card_h - 150, "прав ЄС")
    
    p_box(c, "<b>Ст. 7</b> — приватне і сімейне життя<br/>"
             "<b>Ст. 8</b> — захист персональних даних як окреме право",
          80, card_y + card_h - 168, left_w - 40, size=9, color=TEXT_MUTED, leading=13)
    
    # Two Pills below
    card(c, 80, card_y + 25, 100, 48, bg=CARD_BG_TINT, border=None, rx=6)
    c.setFont("LibSans-Bold", 8.5)
    c.setFillColor(ACCENT_DARK_BLUE)
    c.drawCentredString(130, card_y + 52, "СТ. 7")
    c.drawCentredString(130, card_y + 38, "PRIVACY")
    
    card(c, 195, card_y + 25, 125, 48, bg=CARD_BG_TINT, border=None, rx=6)
    c.setFont("LibSans-Bold", 8.5)
    c.setFillColor(ACCENT_DARK_BLUE)
    c.drawCentredString(257, card_y + 52, "СТ. 8")
    c.drawCentredString(257, card_y + 38, "DATA PROTECTION")
    
    # ---------------- RIGHT CARD: GDPR (Navy Featured) ----------------
    rx_x = 370
    card(c, rx_x, card_y, right_w, card_h, bg=ACCENT_NAVY, border=None, rx=8)
    
    c.setFont("LibSans-Bold", 30)
    c.setFillColor(colors.white)
    c.drawString(rx_x + 30, card_y + card_h - 45, "GDPR")
    
    c.setFont("LibSans", 10.5)
    c.setFillColor(colors.HexColor("#a9bac6"))
    c.drawString(rx_x + 30, card_y + card_h - 70, "Регламент (ЄС) 2016/679 • застосовується з 25 травня 2018")
    
    # 3 Pillars inside GDPR
    p_w = (right_w - 60 - 30) / 3
    pillars = [
        ("01", "Пряма дія", "Регламент прямо застосовується в державах ЄС без потреби внутрішніх законів."),
        ("02", "Поза межами ЄС", "Охоплює пропозицію товарів/послуг або моніторинг людей у межах ЄС."),
        ("03", "Високі штрафи", "До €20 млн або 4% світового річного обороту — залежно від порушення.")
    ]
    
    for p_i, (num, tit, desc) in enumerate(pillars):
        px = rx_x + 30 + p_i * (p_w + 15)
        py = card_y + 110
        card(c, px, py, p_w, 110, bg=colors.HexColor("#20415f"), border=colors.HexColor("#30516d"), rx=6)
        c.setFont("LibSans-Bold", 9.5)
        c.setFillColor(colors.HexColor("#7ed1e6"))
        c.drawString(px + 12, py + 88, num)
        c.setFont("LibSans-Bold", 11)
        c.setFillColor(colors.white)
        c.drawString(px + 12, py + 68, tit)
        p_box(c, desc, px + 12, py + 52, p_w - 24, size=8.5, color=colors.HexColor("#e2e8f0"), leading=12)
    
    # Key Punchline below
    p_box(c, "<b>Ключова зміна: від «конфіденційності» — до контролю особи над тим, як і навіщо обробляються її дані.</b>",
          rx_x + 30, card_y + 60, right_w - 60, size=11.5, color=colors.white, leading=16)

    c.showPage()

# ------------------------------------------------------------------------------
# SLIDE 7: Modern Digital Package (DSA & Political Ads)
# ------------------------------------------------------------------------------
def render_slide_7(c, page_num=7, total_pages=7):
    draw_bg(c)
    draw_hdr(c, f"01–{total_pages:02d}")
    draw_ftr(c, "EUR-Lex — Regulation (EU) 2022/2065 (DSA), Regulation (EU) 2024/900 on political advertising.", str(page_num))
    draw_title_bar(c, f"{page_num:02d}", "Сучасний цифровий пакет ЄС",
                   "DSA + правила політичної реклами: точкові заборони для платформ і таргетингу")
    
    card_y = 60
    card_h = 345
    card_w = 405
    
    # ---------------- LEFT CARD: DSA ----------------
    card(c, 60, card_y, card_w, card_h, bg=CARD_BG_WHITE, border=BORDER_CARD, rx=8)
    
    c.setFont("LibSans-Bold", 26)
    c.setFillColor(TEXT_MAIN)
    c.drawString(85, card_y + card_h - 42, "DSA")
    
    pill(c, 165, card_y + card_h - 42, "2022/2065", bg=ACCENT_NAVY, text_color=colors.white, font_size=9.5, h=22, rx=5, pad_x=12)
    
    c.setFont("LibSans-Bold", 12.5)
    c.setFillColor(TEXT_MAIN)
    c.drawString(85, card_y + card_h - 68, "Digital Services Act")
    
    dsa_items = [
        ("НЕПОВНОЛІТНІ", "Заборона реклами на основі профілювання, якщо платформа з достатньою певністю знає, що користувач — неповнолітній."),
        ("ЧУТЛИВІ ДАНІ", "Заборона профілювальної реклами з використанням спеціальних категорій даних: здоров’я, релігія, політичні погляди тощо."),
        ("DARK PATTERNS", "Інтерфейси не можуть обманювати або маніпулювати вибором користувача (заборона прихованих кнопок та нав'язування).")
    ]
    
    for idx, (label, desc) in enumerate(dsa_items):
        iy = card_y + 195 - idx * 75
        c.setFillColor(ACCENT_BLUE)
        c.circle(96, iy + 22, 9, fill=1, stroke=0)
        
        c.setFont("LibSans-Bold", 9)
        c.setFillColor(ACCENT_NAVY)
        c.drawString(115, iy + 25, label)
        
        p_box(c, desc, 115, iy + 16, card_w - 135, size=8.5, color=TEXT_MUTED, leading=12)
    
    # ---------------- RIGHT CARD: Political Advertising ----------------
    rx_x = 495
    card(c, rx_x, card_y, card_w, card_h, bg=CARD_BG_WHITE, border=BORDER_CARD, rx=8)
    
    c.setFont("LibSans-Bold", 22)
    c.setFillColor(TEXT_MAIN)
    c.drawString(520, card_y + card_h - 40, "Політична реклама")
    
    pill(c, 755, card_y + card_h - 42, "2024/900", bg=ACCENT_BLUE, text_color=colors.white, font_size=9.5, h=22, rx=5, pad_x=12)
    
    c.setFont("LibSans", 11.5)
    c.setFillColor(TEXT_MUTED)
    c.drawString(520, card_y + card_h - 68, "Правила таргетингу та доставки онлайн-реклами")
    
    pol_items = [
        ("01", "Лише дані від самої особи", "Для таргетингу персональні дані мають бути зібрані безпосередньо від суб’єкта (заборона скуплених баз)."),
        ("02", "Окрема явна згода", "Згода на політичний таргетинг має бути <i>explicit</i>, <i>specific</i> і надаватися окремо від згоди на інші сервіси."),
        ("03", "Жодних special categories", "Не можна використовувати чутливі дані, зокрема політичні погляди, релігію, етнічне походження тощо.")
    ]
    
    for idx, (num, tit, desc) in enumerate(pol_items):
        iy = card_y + 195 - idx * 72
        c.setFont("LibSans-Bold", 10.5)
        c.setFillColor(ACCENT_BLUE)
        c.drawString(520, iy + 24, num)
        
        c.setFont("LibSans-Bold", 10.5)
        c.setFillColor(TEXT_MAIN)
        c.drawString(545, iy + 24, tit)
        
        p_box(c, desc, 545, iy + 14, card_w - 75, size=8.5, color=TEXT_MUTED, leading=12)
    
    # Bottom Note Pill inside Right Card
    card(c, 520, card_y + 16, card_w - 45, 26, bg=CARD_BG_TINT, border=None, rx=5)
    c.setFont("LibSans-Bold", 8.2)
    c.setFillColor(ACCENT_DARK_BLUE)
    c.drawCentredString(520 + (card_w - 45) / 2, card_y + 24, "Ухвалено 2024 • основні правила застосовуються з 10.10.2025")

    c.showPage()

# ------------------------------------------------------------------------------
# Main Builder
# ------------------------------------------------------------------------------
def build_presentations():
    # 1. First 4 slides deck
    out_1_4 = "presentation_slides_1_4.pdf"
    c_1_4 = canvas.Canvas(out_1_4, pagesize=PAGESIZE)
    c_1_4.setTitle("Історія права на приватність та захисту персональних даних (Слайди 1–4)")
    c_1_4.setAuthor("Присяжний Савелій, Пашко Ростислав, Олександр Тузюк")
    
    render_slide_1(c_1_4, 1, 4)
    render_slide_2(c_1_4, 2, 4)
    render_slide_3(c_1_4, 3, 4)
    render_slide_4(c_1_4, 4, 4)
    c_1_4.save()
    print(f"Generated {out_1_4} (4 slides)")
    
    # 2. Full 7 slides deck
    out_1_7 = "presentation_full_7_slides.pdf"
    c_1_7 = canvas.Canvas(out_1_7, pagesize=PAGESIZE)
    c_1_7.setTitle("Історія міжнародно-правового становлення права на приватність та захисту персональних даних")
    c_1_7.setAuthor("Присяжний Савелій, Пашко Ростислав, Олександр Тузюк")
    
    render_slide_1(c_1_7, 1, 7)
    render_slide_2(c_1_7, 2, 7)
    render_slide_3(c_1_7, 3, 7)
    render_slide_4(c_1_7, 4, 7)
    render_slide_5(c_1_7, 5, 7)
    render_slide_6(c_1_7, 6, 7)
    render_slide_7(c_1_7, 7, 7)
    c_1_7.save()
    print(f"Generated {out_1_7} (7 slides)")

if __name__ == "__main__":
    build_presentations()
