#!/usr/bin/env python3
"""
Generate a professional 16:9 widescreen presentation PDF for slides 1 to 4.
Uses ReportLab with LiberationSans TrueType fonts for native Ukrainian Cyrillic support.
"""

import os
from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

# Register LiberationSans fonts
FONT_REG = "/usr/share/fonts/liberation-sans-fonts/LiberationSans-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/liberation-sans-fonts/LiberationSans-Bold.ttf"
FONT_ITAL = "/usr/share/fonts/liberation-sans-fonts/LiberationSans-Italic.ttf"

pdfmetrics.registerFont(TTFont("LibSans", FONT_REG))
pdfmetrics.registerFont(TTFont("LibSans-Bold", FONT_BOLD))
pdfmetrics.registerFont(TTFont("LibSans-Italic", FONT_ITAL))

# Slide dimensions (16:9 widescreen: 960 x 540 points)
WIDTH = 960
HEIGHT = 540

# Color Palette
BG_COLOR = colors.HexColor("#0a0f1d")
CARD_BG = colors.HexColor("#131d33")
CARD_BORDER = colors.HexColor("#233554")
TEXT_WHITE = colors.HexColor("#f8fafc")
TEXT_MUTED = colors.HexColor("#94a3b8")
TEXT_BODY = colors.HexColor("#cbd5e1")
ACCENT_BLUE = colors.HexColor("#38bdf8")
ACCENT_NAVY = colors.HexColor("#1d4ed8")
ACCENT_AMBER = colors.HexColor("#f59e0b")
ACCENT_EMERALD = colors.HexColor("#10b981")
ACCENT_PURPLE = colors.HexColor("#a855f7")
ACCENT_ROSE = colors.HexColor("#fb7185")


def draw_background(c):
    """Draw dark slide canvas background."""
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)


def draw_header(c, category, slide_num, total_slides=4):
    """Standard header for content slides."""
    # Top rule
    c.setStrokeColor(colors.HexColor("#1e293b"))
    c.setLineWidth(1)
    c.line(40, HEIGHT - 35, WIDTH - 40, HEIGHT - 35)

    # Category badge
    c.setFont("LibSans-Bold", 9)
    c.setFillColor(ACCENT_BLUE)
    c.drawString(40, HEIGHT - 28, category.upper())

    # Slide Counter
    c.setFont("LibSans", 9)
    c.setFillColor(TEXT_MUTED)
    c.drawRightString(WIDTH - 40, HEIGHT - 28, f"Слайд {slide_num} з {total_slides}")


def draw_footer(c):
    """Standard footer."""
    c.setStrokeColor(colors.HexColor("#1e293b"))
    c.setLineWidth(1)
    c.line(40, 30, WIDTH - 40, 30)

    c.setFont("LibSans", 8.5)
    c.setFillColor(TEXT_MUTED)
    c.drawString(40, 18, "Савелій Присяжний • 2026")
    c.drawRightString(WIDTH - 40, 18, "Міжнародно-правове дослідження: приватність та захист даних")


def draw_card(c, x, y, w, h, bg=CARD_BG, border=CARD_BORDER, rx=10):
    """Draw rounded rectangle container."""
    c.setFillColor(bg)
    c.setStrokeColor(border)
    c.setLineWidth(1.2)
    c.roundRect(x, y, w, h, rx, fill=1, stroke=1)


def p_draw(c, text, x, y, w, font="LibSans", size=10, color=TEXT_BODY, leading=None, align=0, bold=False):
    """Render wrapped text using ReportLab Paragraph."""
    if leading is None:
        leading = size * 1.3
    actual_font = "LibSans-Bold" if bold else font
    style = ParagraphStyle(
        name=f"p_{size}_{actual_font}_{align}",
        fontName=actual_font,
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=align
    )
    p = Paragraph(text, style)
    _, h = p.wrap(w, 500)
    p.drawOn(c, x, y - h)
    return h


# ==============================================================================
# SLIDE 1: Title Slide
# ==============================================================================
def render_slide_1(c):
    draw_background(c)

    # Decorative top bar
    c.setFillColor(ACCENT_BLUE)
    c.rect(0, HEIGHT - 6, WIDTH, 6, fill=1, stroke=0)

    # Header
    c.setFont("LibSans-Bold", 11)
    c.setFillColor(ACCENT_BLUE)
    c.drawString(60, HEIGHT - 45, "МІЖНАРОДНО-ПРАВОВЕ ДОСЛІДЖЕННЯ")
    c.setFont("LibSans", 9.5)
    c.setFillColor(TEXT_MUTED)
    c.drawString(60, HEIGHT - 60, "Європейські стандарти приватності та захисту персональних даних")

    # Flag of Europe on the right
    flag_path = "slide-01/flag_of_europe.png"
    if os.path.exists(flag_path):
        c.drawImage(flag_path, WIDTH - 130, HEIGHT - 75, width=70, height=46.6, preserveAspectRatio=True, mask='auto')

    # Main Title Container
    draw_card(c, 60, 215, WIDTH - 120, 240, bg=colors.HexColor("#10182b"), border=colors.HexColor("#2a3f66"), rx=14)

    # Badge inside title container
    c.setFillColor(colors.HexColor("#1e3a8a"))
    c.roundRect(85, 410, 255, 24, 6, fill=1, stroke=0)
    c.setFont("LibSans-Bold", 9.5)
    c.setFillColor(colors.HexColor("#93c5fd"))
    c.drawString(97, 417, "МІЖНАРОДНО-ПРАВОВЕ ДОСЛІДЖЕННЯ")

    # Big Title
    p_draw(c, "Історія міжнародно-правового становлення права на приватність та захисту персональних даних",
           85, 395, WIDTH - 170, font="LibSans-Bold", size=23, color=TEXT_WHITE, leading=30)

    # Subtitle
    p_draw(c, "Від перших міжнародних гарантій середини XX століття до цифрового суверенітету особи, GDPR та штучного інтелекту",
           85, 315, WIDTH - 170, font="LibSans", size=13, color=ACCENT_BLUE, leading=18)

    # Info chips inside container
    c.setStrokeColor(colors.HexColor("#233554"))
    c.setLineWidth(1)
    c.line(85, 275, WIDTH - 85, 275)

    c.setFont("LibSans-Bold", 10.5)
    c.setFillColor(TEXT_WHITE)
    c.drawString(85, 245, "Доповідачі:")
    c.setFont("LibSans-Bold", 10.5)
    c.setFillColor(ACCENT_BLUE)
    c.drawString(170, 245, "Присяжний Савелій (ІМ-55) • Пашко Ростислав (ІП-53) • Олександр Тузюк (ІО-53)")

    # Bottom Timeline Bar
    draw_card(c, 60, 50, WIDTH - 120, 140, bg=colors.HexColor("#0d1527"), border=colors.HexColor("#1e293b"), rx=10)

    c.setFont("LibSans-Bold", 10.5)
    c.setFillColor(ACCENT_AMBER)
    c.drawString(85, 162, "КЛЮЧОВИЙ ХРОНОЛОГІЧНИЙ МАРШРУТ ДОПОВІДІ:")

    # Milestone boxes
    milestones = [
        ("1890", "Воррен & Брандейс", "Harvard Law Review"),
        ("1948", "ЗДПЛ ООН (ст. 12)", "1-ше закріплення"),
        ("1950", "ЄКПЛ (ст. 8)", "Судовий захист ЄСПЛ"),
        ("1981", "Конвенція № 108", "1-й договір про дані"),
        ("2000", "Хартія ЄС (ст. 7/8)", "Розділення прав"),
        ("2016", "GDPR (ЄС 2016/679)", "Золотий стандарт"),
        ("2024+", "DSA & AI Act", "Алгоритми і ШІ")
    ]

    col_w = (WIDTH - 170) / len(milestones)
    for i, (year, title, desc) in enumerate(milestones):
        x = 85 + i * col_w
        c.setFillColor(colors.HexColor("#172554") if i % 2 == 0 else colors.HexColor("#1e1b4b"))
        c.roundRect(x, 65, col_w - 8, 80, 6, fill=1, stroke=0)

        # Year badge
        c.setFont("LibSans-Bold", 12)
        c.setFillColor(ACCENT_AMBER if "2024" in year or "1948" in year or "1981" in year else ACCENT_BLUE)
        c.drawString(x + 8, 126, year)

        # Title
        c.setFont("LibSans-Bold", 8.5)
        c.setFillColor(TEXT_WHITE)
        c.drawString(x + 8, 106, title)

        # Desc
        c.setFont("LibSans", 7.5)
        c.setFillColor(TEXT_MUTED)
        c.drawString(x + 8, 88, desc)

    c.showPage()


# ==============================================================================
# SLIDE 2: Privacy vs Data Protection
# ==============================================================================
def render_slide_2(c):
    draw_background(c)
    draw_header(c, "Концептуальні засади • Розмежування понять", 2)
    draw_footer(c)

    # Slide Title
    p_draw(c, "Право на приватність ≠ Захист персональних даних",
           40, HEIGHT - 50, WIDTH - 80, font="LibSans-Bold", size=20, color=TEXT_WHITE)
    p_draw(c, "Чому приватність ширша за конфіденційність, а захист даних є самостійним позитивним правом",
           40, HEIGHT - 76, WIDTH - 80, font="LibSans", size=11.5, color=ACCENT_BLUE)

    card_w = (WIDTH - 100) / 2
    card_h = 320
    card_y = 110

    # ------------------ LEFT CARD: PRIVACY ------------------
    draw_card(c, 40, card_y, card_w, card_h, bg=colors.HexColor("#0f1c38"), border=colors.HexColor("#2563eb"), rx=12)

    # Header bar
    c.setFillColor(colors.HexColor("#1e3a8a"))
    c.roundRect(40, card_y + card_h - 45, card_w, 45, 12, fill=1, stroke=0)
    c.rect(40, card_y + card_h - 45, card_w, 15, fill=1, stroke=0)

    # Badge Left
    badge_w = 98
    badge_h = 20
    bx = 40 + card_w - badge_w - 14
    by = card_y + card_h - 33
    c.setFillColor(colors.HexColor("#172554"))
    c.roundRect(bx, by, badge_w, badge_h, 4, fill=1, stroke=0)
    c.setFont("LibSans-Bold", 7.5)
    c.setFillColor(colors.HexColor("#93c5fd"))
    c.drawCentredString(bx + badge_w / 2, by + 6, "НЕГАТИВНЕ ПРАВО")

    # Title Left
    c.setFont("LibSans-Bold", 12.5)
    c.setFillColor(TEXT_WHITE)
    c.drawString(56, card_y + card_h - 28, "1. Право на приватність (Privacy)")

    # Essence
    p_draw(c, "<b>Сутність:</b> «Право бути залишеним у спокої» <i>(The right to be let alone)</i>. Право особи самостійно визначати, коли, як і скільки інформації про себе розкривати іншим (Алан Вестін, 1967).",
           60, card_y + card_h - 58, card_w - 40, size=9.5, color=TEXT_BODY, leading=13.5)

    # 4 Components
    c.setFont("LibSans-Bold", 9.5)
    c.setFillColor(ACCENT_BLUE)
    c.drawString(60, card_y + 195, "4 складові приватності (за матеріалами курсу):")

    comp_items = [
        ("Усамітнення (solitude):", "відокремленість від спільноти, відсутність стороннього нагляду"),
        ("Анонімність (anonymity):", "можливість діяти публічно, не будучи ідентифікованим"),
        ("Інтимність (intimacy):", "право на довірливі стосунки у вузькому колі близьких"),
        ("Збереження таємниці (reserve):", "самостійне обмеження розкриття відомостей про себе")
    ]
    for idx, (label, desc) in enumerate(comp_items):
        cy = card_y + 175 - idx * 19
        c.setFillColor(ACCENT_BLUE)
        c.circle(68, cy + 3, 2.5, fill=1, stroke=0)
        c.setFont("LibSans-Bold", 8.5)
        c.setFillColor(TEXT_WHITE)
        c.drawString(78, cy, label)
        c.setFont("LibSans", 8.5)
        c.setFillColor(TEXT_BODY)
        c.drawString(78 + c.stringWidth(label, "LibSans-Bold", 8.5) + 4, cy, desc)

    # 4 Dimensions
    c.setFont("LibSans-Bold", 9.5)
    c.setFillColor(ACCENT_BLUE)
    c.drawString(60, card_y + 90, "4 види приватності:")
    p_draw(c, "• <b>Тілесна:</b> фізична недоторканність від примусових медичних процедур.<br/>"
              "• <b>Територіальна:</b> захист житла, робочого місця, автомобіля від обшуку.<br/>"
              "• <b>Комунікаційна:</b> таємниця кореспонденції, дзвінків, чатів у месенджерах.<br/>"
              "• <b>Інформаційна:</b> правила збору та обробки відомостей про людину.",
           60, card_y + 75, card_w - 40, size=8.5, color=TEXT_BODY, leading=12)

    # Footer banner
    c.setFillColor(colors.HexColor("#081226"))
    c.roundRect(50, card_y + 8, card_w - 20, 22, 5, fill=1, stroke=0)
    c.setFont("LibSans-Bold", 8)
    c.setFillColor(colors.HexColor("#93c5fd"))
    c.drawString(60, card_y + 15, "Нормативні якорі: ст. 12 ЗДПЛ 1948 • ст. 8 ЄКПЛ 1950 • ст. 7 Хартії ЄС 2000")

    # ------------------ RIGHT CARD: DATA PROTECTION ------------------
    rx_x = 40 + card_w + 20
    draw_card(c, rx_x, card_y, card_w, card_h, bg=colors.HexColor("#0a261c"), border=colors.HexColor("#059669"), rx=12)

    # Header bar
    c.setFillColor(colors.HexColor("#047857"))
    c.roundRect(rx_x, card_y + card_h - 45, card_w, 45, 12, fill=1, stroke=0)
    c.rect(rx_x, card_y + card_h - 45, card_w, 15, fill=1, stroke=0)

    # Badge Right
    badge_w = 98
    badge_h = 20
    bx = rx_x + card_w - badge_w - 14
    by = card_y + card_h - 33
    c.setFillColor(colors.HexColor("#064e3b"))
    c.roundRect(bx, by, badge_w, badge_h, 4, fill=1, stroke=0)
    c.setFont("LibSans-Bold", 7.5)
    c.setFillColor(colors.HexColor("#a7f3d0"))
    c.drawCentredString(bx + badge_w / 2, by + 6, "ПОЗИТИВНЕ ПРАВО")

    # Title Right
    c.setFont("LibSans-Bold", 12.5)
    c.setFillColor(TEXT_WHITE)
    c.drawString(rx_x + 16, card_y + card_h - 28, "2. Захист даних (Data Protection)")

    # Definition
    p_draw(c, "<b>Легальна дефініція (ст. 2 ЗУ «Про захист ПД», ст. 4 GDPR):</b> будь-яка інформація про фізичну особу, яка <b>ідентифікована або може бути конкретно ідентифікована</b> (безпосередньо за іменем або опосередковано за ID, IP, геолокацією чи біометрією).",
           rx_x + 20, card_y + card_h - 58, card_w - 40, size=9.5, color=TEXT_BODY, leading=13.5)

    # Regulatory features
    c.setFont("LibSans-Bold", 9.5)
    c.setFillColor(ACCENT_EMERALD)
    c.drawString(rx_x + 20, card_y + 195, "Ключові нормативні імперативи захисту даних:")

    dp_items = [
        ("Законність та мета:", "обробка дозволена лише за наявності згоди або законної підстави"),
        ("Прозорість (transparency):", "обов'язок володільця сповіщати про мету та обсяг обробки"),
        ("Права суб'єкта даних:", "право на доступ, виправлення, видалення («право на забуття»)"),
        ("Інституційний нагляд:", "обов'язковий контроль незалежного наглядового органу (DPA)")
    ]
    for idx, (label, desc) in enumerate(dp_items):
        cy = card_y + 175 - idx * 19
        c.setFillColor(ACCENT_EMERALD)
        c.circle(rx_x + 28, cy + 3, 2.5, fill=1, stroke=0)
        c.setFont("LibSans-Bold", 8.5)
        c.setFillColor(TEXT_WHITE)
        c.drawString(rx_x + 38, cy, label)
        c.setFont("LibSans", 8.5)
        c.setFillColor(TEXT_BODY)
        c.drawString(rx_x + 38 + c.stringWidth(label, "LibSans-Bold", 8.5) + 4, cy, desc)

    # Crucial Distinction
    draw_card(c, rx_x + 15, card_y + 38, card_w - 30, 68, bg=colors.HexColor("#063b2c"), border=colors.HexColor("#10b981"), rx=6)
    p_draw(c, "<b>Право на приватність ≠ Конфіденційність:</b><br/>"
              "Приватність — це свобода вибору (розкривати себе чи ні). Публікація фото у соцмережах є реалізацією приватності, а не її втратою. Захист даних гарантує законність подальшої обробки цих фото алгоритмами.",
           rx_x + 25, card_y + 96, card_w - 50, size=8.5, color=colors.HexColor("#e2e8f0"), leading=12)

    # Footer banner
    c.setFillColor(colors.HexColor("#051c14"))
    c.roundRect(rx_x + 10, card_y + 8, card_w - 20, 22, 5, fill=1, stroke=0)
    c.setFont("LibSans-Bold", 8)
    c.setFillColor(colors.HexColor("#6ee7b7"))
    c.drawString(rx_x + 20, card_y + 15, "Нормативні якорі: Конвенція 108/108+ • ст. 8 Хартії ЄС • GDPR 2016/679")

    # Bottom summary pill
    draw_card(c, 40, 42, WIDTH - 80, 56, bg=colors.HexColor("#1e293b"), border=colors.HexColor("#334155"), rx=8)
    p_draw(c, "<b>Ключовий висновок для виступу:</b> Приватність захищає внутрішній та фізичний життєвий простір людини від проникнення влади чи сторонніх осіб («залиште мене у спокої»). Натомість захист даних вступає в силу тоді, коли інформація про людину вже зібрана або стала публічною — він забезпечує правила її обігу, захищаючи від свавільного профілювання та дискримінації.",
           55, 90, WIDTH - 110, size=9.5, color=colors.HexColor("#e2e8f0"), leading=13.5)

    c.showPage()


# ==============================================================================
# SLIDE 3: Warren & Brandeis 1890
# ==============================================================================
def render_slide_3(c):
    draw_background(c)
    draw_header(c, "Доктринальні витоки • 1890 рік", 3)
    draw_footer(c)

    # Slide Title
    p_draw(c, "Доктринальні витоки: стаття Воррена і Брандейса (1890 р.)",
           40, HEIGHT - 50, WIDTH - 80, font="LibSans-Bold", size=20, color=TEXT_WHITE)
    p_draw(c, "Як винахід компактної камери Kodak Джорджа Істмена спричинив народження концепції «The Right to be Let Alone»",
           40, HEIGHT - 76, WIDTH - 80, font="LibSans", size=11.5, color=ACCENT_AMBER)

    left_w = 260
    left_x = 40
    right_x = left_x + left_w + 20
    right_w = WIDTH - 40 - right_x

    # ------------------ LEFT COLUMN: PORTRAIT & BIO ------------------
    draw_card(c, left_x, 45, left_w, 395, bg=colors.HexColor("#141824"), border=colors.HexColor("#2a354f"), rx=12)

    # Image
    brandeis_img = "slide-03/louis_brandeis_1915.jpg"
    if os.path.exists(brandeis_img):
        c.drawImage(brandeis_img, left_x + 25, 230, width=210, height=195, preserveAspectRatio=True, mask='auto')

    c.setFont("LibSans-Bold", 12)
    c.setFillColor(TEXT_WHITE)
    c.drawString(left_x + 20, 215, "Луїс Д. Брандейс (1856–1941)")
    c.setFont("LibSans-Italic", 9)
    c.setFillColor(ACCENT_AMBER)
    c.drawString(left_x + 20, 200, "Співавтор статті, суддя Верховного Суду США")

    p_draw(c, "<b>Публікація:</b> <i>«The Right to Privacy»</i><br/>"
              "<b>Журнал:</b> Harvard Law Review, Vol. 4, No. 5<br/>"
              "<b>Точна дата:</b> 15 грудня 1890 року.<br/><br/>"
              "<b>Співавтор:</b> <b>Семюель Д. Воррен</b> (бостонський юрист, кращий випускник Гарварду 1877 р.).<br/><br/>"
              "Найбільш цитована наукова стаття з юриспруденції в історії загального права.",
           left_x + 20, 185, left_w - 40, size=9, color=TEXT_BODY, leading=13)

    # ------------------ RIGHT COLUMN: 3 PILLARS ------------------
    col_h = 120
    gap = 12

    # Card 1: Tech Trigger
    c1_y = 45 + 2 * (col_h + gap) + 10
    draw_card(c, right_x, c1_y, right_w, col_h, bg=colors.HexColor("#181829"), border=colors.HexColor("#d97706"), rx=10)
    c.setFillColor(colors.HexColor("#b45309"))
    c.roundRect(right_x, c1_y + col_h - 26, 170, 26, 6, fill=1, stroke=0)
    c.setFont("LibSans-Bold", 9)
    c.setFillColor(TEXT_WHITE)
    c.drawString(right_x + 12, c1_y + col_h - 18, "1. ТЕХНОЛОГІЧНИЙ ТРИГЕР")

    p_draw(c, "<b>1888 рік — поява камери Kodak:</b> Джордж Істмен запатентував першу ручну фотокамеру з плівкою під слоганом <i>«You press the button, we do the rest»</i>. Фотографія вийшла зі студій на вулиці — знімати людину стало можливим непомітно, миттєво і без її згоди.<br/>"
              "<b>«Жовта преса»:</b> Бостонська газета <i>The Saturday Evening Gazette</i> почала публікувати плітки та фотографії про приватне життя родини Воррена. Старе право захищало лише паркан (делікт <i>trespass</i>) чи вкрадені речі (власність), але не душевний спокій.",
           right_x + 15, c1_y + col_h - 35, right_w - 30, size=9.5, color=TEXT_BODY, leading=13.5)

    # Card 2: Legal Formula
    c2_y = 45 + col_h + gap + 5
    draw_card(c, right_x, c2_y, right_w, col_h, bg=colors.HexColor("#0e2238"), border=colors.HexColor("#0284c7"), rx=10)
    c.setFillColor(colors.HexColor("#0369a1"))
    c.roundRect(right_x, c2_y + col_h - 26, 235, 26, 6, fill=1, stroke=0)
    c.setFont("LibSans-Bold", 9)
    c.setFillColor(TEXT_WHITE)
    c.drawString(right_x + 12, c2_y + col_h - 18, "2. «THE RIGHT TO BE LET ALONE»")

    p_draw(c, "<b>Формула судді Томаса Кулі:</b> Воррен і Брандейс запозичили вислів із трактату <i>«A Treatise on the Law of Torts»</i> (1879 р., с. 29): <i>«The right to one's person may be said to be a right of complete immunity: to be let alone»</i>.<br/>"
              "<b>Головна ідея:</b> Право має визнати, що людина має право <b>«бути залишеною у спокої»</b>. Спроби таблоїдів комерціалізувати чуже приватне життя — це не просто порушення етики, це цивільне правопорушення, що завдає особі моральної шкоди.",
           right_x + 15, c2_y + col_h - 35, right_w - 30, size=9.5, color=TEXT_BODY, leading=13.5)

    # Card 3: Paradigm Shift
    c3_y = 45
    draw_card(c, right_x, c3_y, right_w, col_h, bg=colors.HexColor("#0c291d"), border=colors.HexColor("#059669"), rx=10)
    c.setFillColor(colors.HexColor("#047857"))
    c.roundRect(right_x, c3_y + col_h - 26, 210, 26, 6, fill=1, stroke=0)
    c.setFont("LibSans-Bold", 9)
    c.setFillColor(TEXT_WHITE)
    c.drawString(right_x + 12, c3_y + col_h - 18, "3. ЗМІНА ПРАВОВОЇ ПАРАДИГМИ")

    p_draw(c, "<b>Еволюція концепції власності до захисту особистості:</b><br/>"
              "• <i>Старе право:</i> захист фізичного життя → захист речового майна і землі → захист авторського права.<br/>"
              "• <i>Нове право Воррена і Брандейса:</i> захист духовної та психологічної цілісності — <b>«недоторканності людської особистості» <i>(inviolate personality)</i></b>.<br/>"
              "<b>Історичний міст:</b> Саме ця стаття заклала доктринальне підґрунтя, з якого у 1948 році виросла стаття 12 Загальної декларації прав людини ООН.",
           right_x + 15, c3_y + col_h - 35, right_w - 30, size=9.5, color=TEXT_BODY, leading=13.5)

    c.showPage()


# ==============================================================================
# SLIDE 4: UDHR 1948 & ECHR 1950 (Case law)
# ==============================================================================
def render_slide_4(c):
    draw_background(c)
    draw_header(c, "Міжнародно-правове закріплення • 1948–1950", 4)
    draw_footer(c)

    # Slide Title
    p_draw(c, "Перші міжнародні акти: ЗДПЛ 1948 та Конвенція Ради Європи 1950",
           40, HEIGHT - 50, WIDTH - 80, font="LibSans-Bold", size=20, color=TEXT_WHITE)
    p_draw(c, "Перше міжнародне закріплення (ст. 12 ЗДПЛ), трискладовий тест (ст. 8 ЄКПЛ) та судова практика ЄСПЛ",
           40, HEIGHT - 76, WIDTH - 80, font="LibSans", size=11.5, color=ACCENT_BLUE)

    col_w = (WIDTH - 120) / 3
    col_h = 390
    col_y = 45

    # ------------------ COL 1: UDHR 1948 ------------------
    c1_x = 40
    draw_card(c, c1_x, col_y, col_w, col_h, bg=colors.HexColor("#121b2f"), border=colors.HexColor("#2563eb"), rx=10)

    # Header
    c.setFillColor(colors.HexColor("#1d4ed8"))
    c.roundRect(c1_x, col_y + col_h - 35, col_w, 35, 10, fill=1, stroke=0)
    c.rect(c1_x, col_y + col_h - 35, col_w, 10, fill=1, stroke=0)
    c.setFont("LibSans-Bold", 10.5)
    c.setFillColor(TEXT_WHITE)
    c.drawString(c1_x + 12, col_y + col_h - 22, "1. ДЕ ЗАКРІПЛЕНО ВПЕРШЕ У СВІТІ?")

    # Image
    eleanor_img = "slide-04/eleanor_roosevelt_udhr_opt.jpg"
    if os.path.exists(eleanor_img):
        c.drawImage(eleanor_img, c1_x + 15, col_y + col_h - 170, width=col_w - 30, height=125, preserveAspectRatio=True, mask='auto')

    c.setFont("LibSans-Bold", 9)
    c.setFillColor(ACCENT_AMBER)
    c.drawString(c1_x + 15, col_y + col_h - 182, "Загальна декларація прав людини (ЗДПЛ)")
    c.setFont("LibSans-Italic", 7.5)
    c.setFillColor(TEXT_MUTED)
    c.drawString(c1_x + 15, col_y + col_h - 194, "10 грудня 1948 р., Париж, Генеральна Асамблея ООН")

    # Text of Art 12
    draw_card(c, c1_x + 10, col_y + 10, col_w - 20, 180, bg=colors.HexColor("#0b1324"), border=colors.HexColor("#1e293b"), rx=6)
    p_draw(c, "<b>Стаття 12 ЗДПЛ 1948 року:</b><br/>"
              "<i>«Ніхто не може зазнавати безпідставного втручання в його особисте і сімейне життя, безпідставного посягання на недоторканність його житла, таємницю його кореспонденції або на його честь і репутацію.<br/>"
              "Кожна людина має право на захист закону від такого втручання або таких посягань».</i><br/><br/>"
              "• <b>Історичний контекст:</b> відповідь людства на тоталітарне поліцейське свавілля Другої світової війни.<br/>"
              "• <b>Характер:</b> перший універсальний стандарт прав людини.",
           c1_x + 18, col_y + 180, col_w - 36, size=8.5, color=TEXT_BODY, leading=12)

    # ------------------ COL 2: ECHR 1950 & 3-PART TEST ------------------
    c2_x = c1_x + col_w + 20
    draw_card(c, c2_x, col_y, col_w, col_h, bg=colors.HexColor("#0f2136"), border=colors.HexColor("#0284c7"), rx=10)

    # Header
    c.setFillColor(colors.HexColor("#0369a1"))
    c.roundRect(c2_x, col_y + col_h - 35, col_w, 35, 10, fill=1, stroke=0)
    c.rect(c2_x, col_y + col_h - 35, col_w, 10, fill=1, stroke=0)
    c.setFont("LibSans-Bold", 10.5)
    c.setFillColor(TEXT_WHITE)
    c.drawString(c2_x + 12, col_y + col_h - 22, "2. ЄКПЛ 1950: СТАТТЯ 8 ТА ТЕСТ")

    p_draw(c, "<b>Конвенція Ради Європи 1950 р. (ЄКПЛ):</b><br/>"
              "Перший <b>юридично обов'язковий</b> регіональний договір із прямим механізмом судового захисту (ЄСПЛ).<br/><br/>"
              "<b>Стаття 8 ч. 1:</b> Кожен має право на повагу до свого приватного і сімейного життя, житла та кореспонденції.<br/><br/>"
              "<b>Трискладовий тест втручання (ч. 2 ст. 8):</b><br/>"
              "Держава може втручатися <b>виключно за трьох умов одночасно:</b>",
           c2_x + 15, col_y + col_h - 45, col_w - 30, size=9, color=TEXT_BODY, leading=13)

    # 3 Steps boxes
    steps = [
        ("1. Згідно із законом", "In accordance with the law: доступність, чіткість та передбачуваність норми"),
        ("2. Легітимна мета", "Legitimate aim: безпека, добробут, запобігання злочинам, захист прав інших"),
        ("3. Необхідно в суспільстві", "Necessary in democratic society: нагальна потреба та пропорційність")
    ]
    for idx, (st_title, st_desc) in enumerate(steps):
        sy = col_y + 148 - idx * 50
        draw_card(c, c2_x + 12, sy, col_w - 24, 42, bg=colors.HexColor("#091728"), border=colors.HexColor("#0ea5e9"), rx=5)
        c.setFont("LibSans-Bold", 8.5)
        c.setFillColor(ACCENT_BLUE)
        c.drawString(c2_x + 20, sy + 29, st_title)
        p_draw(c, st_desc, c2_x + 20, sy + 23, col_w - 40, size=7.5, color=TEXT_BODY, leading=9.5)

    # Note
    draw_card(c, c2_x + 12, col_y + 10, col_w - 24, 26, bg=colors.HexColor("#091728"), border=colors.HexColor("#1e293b"), rx=5)
    p_draw(c, "<b>Також закріплено:</b> ст. 17 МПГПП ООН 1966 р.",
           c2_x + 18, col_y + 27, col_w - 36, size=7.5, color=colors.HexColor("#94a3b8"), leading=9)

    # ------------------ COL 3: ECTHR PRECEDENTS ------------------
    c3_x = c2_x + col_w + 20
    draw_card(c, c3_x, col_y, col_w, col_h, bg=colors.HexColor("#1b1833"), border=colors.HexColor("#a855f7"), rx=10)

    # Header
    c.setFillColor(colors.HexColor("#7e22ce"))
    c.roundRect(c3_x, col_y + col_h - 35, col_w, 35, 10, fill=1, stroke=0)
    c.rect(c3_x, col_y + col_h - 35, col_w, 10, fill=1, stroke=0)
    c.setFont("LibSans-Bold", 10.5)
    c.setFillColor(TEXT_WHITE)
    c.drawString(c3_x + 12, col_y + col_h - 22, "3. СУДОВА ПРАКТИКА ЄСПЛ")

    p_draw(c, "ЄСПЛ розглядає Конвенцію як «живий інструмент» <i>(living instrument)</i>, що поширив ст. 8 на збереження баз даних:",
           c3_x + 15, col_y + col_h - 45, col_w - 30, size=9, color=TEXT_BODY, leading=12.5)

    cases = [
        ("Leander v. Sweden (1987)",
         "<b>Таємні картотеки безпеки:</b><br/>"
         "ЄСПЛ уперше чітко встановив: збереження та передача публічними органами інформації про особу в таємних реєстрах безпеки є <b>втручанням у ст. 8 ЄКПЛ</b>."),

        ("Amann v. Switzerland (2000)",
         "<b>Вихід за межі «усамітнення»:</b><br/>"
         "Велика Палата зазначила: приватне життя не зводиться до внутрішнього кола <i>(inner circle)</i>. Воно охоплює <b>право на професійну, ділову та комерційну діяльність</b>."),

        ("Rotaru v. Romania (2000)",
         "<b>Досьє спецслужб з відкритих даних:</b><br/>"
         "Навіть якщо дані є публічними, їх систематизація та накопичення в досьє спецслужб порушує ст. 8, якщо особі не надано права ознайомитися з ними та спростувати неправду.")
    ]

    for idx, (c_title, c_text) in enumerate(cases):
        cy = col_y + 205 - idx * 95
        draw_card(c, c3_x + 12, cy, col_w - 24, 88, bg=colors.HexColor("#120f24"), border=colors.HexColor("#9333ea"), rx=6)
        c.setFont("LibSans-Bold", 9)
        c.setFillColor(ACCENT_PURPLE)
        c.drawString(c3_x + 20, cy + 74, c_title)
        p_draw(c, c_text, c3_x + 20, cy + 68, col_w - 40, size=8, color=TEXT_BODY, leading=11)

    c.showPage()


def main():
    pdf_filename = "presentation_slides_1_4_dark.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=(WIDTH, HEIGHT))
    c.setTitle("Історія міжнародно-правового становлення права на приватність та захисту персональних даних")
    c.setAuthor("Присяжний Савелій, Пашко Ростислав, Олександр Тузюк")
    c.setSubject("Міжнародно-правове дослідження: стандарти ЄС та Ради Європи")

    render_slide_1(c)
    render_slide_2(c)
    render_slide_3(c)
    render_slide_4(c)

    c.save()
    print(f"Presentation successfully saved to {pdf_filename}")


if __name__ == "__main__":
    main()
