from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable

import fitz
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTFont
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    DecodedStreamObject,
    DictionaryObject,
    FloatObject,
    NameObject,
    RectangleObject,
    TextStringObject,
)
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


TRIM_W_MM = 90.0
TRIM_H_MM = 50.0
BLEED_MM = 3.0
MEDIA_W = (TRIM_W_MM + 2 * BLEED_MM) * mm
MEDIA_H = (TRIM_H_MM + 2 * BLEED_MM) * mm
BLEED = BLEED_MM * mm
TRIM_W = TRIM_W_MM * mm
TRIM_H = TRIM_H_MM * mm

OUT_DIR = Path.home() / "Downloads" / "Cartoes Jus9 Redesenho Vetorial CMYK"
PREVIEW_DIR = OUT_DIR / "previews"
ICC_PROFILE = Path(r"C:\Windows\System32\spool\drivers\color\RSWOP.icm")

FONT_SERIF = Path(r"C:\Windows\Fonts\georgia.ttf")
FONT_SERIF_BOLD = Path(r"C:\Windows\Fonts\georgiab.ttf")
FONT_SANS = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_SANS_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")

RICH_BLACK = (0.78, 0.64, 0.52, 0.94)
DEEP_BLACK = (0.86, 0.70, 0.56, 0.98)
BLACK_2 = (0.74, 0.61, 0.49, 0.91)
GOLD = (0.06, 0.20, 0.96, 0.02)
GOLD_DARK = (0.14, 0.34, 0.90, 0.16)
GOLD_LIGHT = (0.00, 0.08, 0.54, 0.00)
COPPER = (0.08, 0.54, 0.92, 0.08)
WHITE = (0.00, 0.00, 0.02, 0.00)
MUTED_WHITE = (0.06, 0.06, 0.11, 0.02)
SUBTLE = (0.44, 0.38, 0.28, 0.76)


class OutlineFont:
    def __init__(self, path: Path):
        self.path = path
        self.font = TTFont(path)
        self.glyph_set = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap()
        self.hmtx = self.font["hmtx"].metrics
        self.units_per_em = self.font["head"].unitsPerEm
        self.space_width = self.hmtx.get("space", (self.units_per_em // 3, 0))[0]

    def glyph_name(self, char: str) -> str:
        return self.cmap.get(ord(char), ".notdef")

    def text_width(
        self,
        text: str,
        size: float,
        tracking: float = 0.0,
        horizontal_scale: float = 1.0,
    ) -> float:
        scale = size / self.units_per_em * horizontal_scale
        total = 0.0
        for index, char in enumerate(text):
            if char == "\n":
                continue
            glyph_name = self.glyph_name(char)
            advance = self.hmtx.get(glyph_name, (self.space_width, 0))[0]
            total += advance * scale
            if index != len(text) - 1:
                total += tracking
        return total

    def draw(
        self,
        c: canvas.Canvas,
        text: str,
        x: float,
        y: float,
        size: float,
        fill: tuple[float, float, float, float],
        tracking: float = 0.0,
        horizontal_scale: float = 1.0,
        centered: bool = False,
        stroke: tuple[float, float, float, float] | None = None,
        stroke_width: float = 0.0,
    ) -> None:
        if centered:
            x -= self.text_width(text, size, tracking, horizontal_scale) / 2
        scale = size / self.units_per_em
        c.setFillColorCMYK(*fill)
        if stroke:
            c.setStrokeColorCMYK(*stroke)
            c.setLineWidth(stroke_width)
        cursor = x
        for index, char in enumerate(text):
            glyph_name = self.glyph_name(char)
            glyph = self.glyph_set[glyph_name]
            pen = DecomposingRecordingPen(self.glyph_set)
            glyph.draw(pen)
            path = c.beginPath()
            current_point: tuple[float, float] | None = None
            for operator, args in pen.value:
                if operator == "moveTo":
                    px, py = args[0]
                    current_point = (cursor + px * scale * horizontal_scale, y + py * scale)
                    path.moveTo(*current_point)
                elif operator == "lineTo":
                    px, py = args[0]
                    current_point = (cursor + px * scale * horizontal_scale, y + py * scale)
                    path.lineTo(*current_point)
                elif operator == "qCurveTo":
                    if current_point is None:
                        continue
                    points = list(args)
                    if not points:
                        continue
                    if points[-1] is None:
                        points = points[:-1]
                    if not points:
                        continue
                    if len(points) == 1:
                        px, py = points[0]
                        current_point = (cursor + px * scale * horizontal_scale, y + py * scale)
                        path.lineTo(*current_point)
                    else:
                        start_x, start_y = current_point
                        for point_index in range(len(points) - 1):
                            qx, qy = points[point_index]
                            if point_index == len(points) - 2:
                                ex, ey = points[point_index + 1]
                            else:
                                nx, ny = points[point_index + 1]
                                ex, ey = (qx + nx) / 2, (qy + ny) / 2
                            cx1 = start_x + (2 / 3) * (
                                cursor + qx * scale * horizontal_scale - start_x
                            )
                            cy1 = start_y + (2 / 3) * (y + qy * scale - start_y)
                            end_x = cursor + ex * scale * horizontal_scale
                            end_y = y + ey * scale
                            cx2 = end_x + (2 / 3) * (
                                cursor + qx * scale * horizontal_scale - end_x
                            )
                            cy2 = end_y + (2 / 3) * (y + qy * scale - end_y)
                            path.curveTo(cx1, cy1, cx2, cy2, end_x, end_y)
                            start_x, start_y = end_x, end_y
                        current_point = (start_x, start_y)
                elif operator == "curveTo":
                    p1, p2, p3 = args
                    current_point = (
                        cursor + p3[0] * scale * horizontal_scale,
                        y + p3[1] * scale,
                    )
                    path.curveTo(
                        cursor + p1[0] * scale * horizontal_scale,
                        y + p1[1] * scale,
                        cursor + p2[0] * scale * horizontal_scale,
                        y + p2[1] * scale,
                        *current_point,
                    )
                elif operator == "closePath":
                    path.close()
                    current_point = None
            c.drawPath(path, stroke=1 if stroke else 0, fill=1)
            advance = self.hmtx.get(glyph_name, (self.space_width, 0))[0]
            cursor += advance * scale * horizontal_scale
            if index != len(text) - 1:
                cursor += tracking

    def draw_mirrored(
        self,
        c: canvas.Canvas,
        text: str,
        right_edge_x: float,
        y: float,
        size: float,
        fill: tuple[float, float, float, float],
        tracking: float = 0.0,
        horizontal_scale: float = 1.0,
        stroke: tuple[float, float, float, float] | None = None,
        stroke_width: float = 0.0,
    ) -> None:
        c.saveState()
        c.scale(-1, 1)
        self.draw(
            c,
            text,
            -right_edge_x,
            y,
            size,
            fill,
            tracking=tracking,
            horizontal_scale=horizontal_scale,
            stroke=stroke,
            stroke_width=stroke_width,
        )
        c.restoreState()


def set_fill(c: canvas.Canvas, color: tuple[float, float, float, float]) -> None:
    c.setFillColorCMYK(*color)


def set_stroke(
    c: canvas.Canvas,
    color: tuple[float, float, float, float],
    width: float = 0.4,
) -> None:
    c.setStrokeColorCMYK(*color)
    c.setLineWidth(width)


def rounded_card_path(c: canvas.Canvas, x: float, y: float, w: float, h: float, r: float):
    path = c.beginPath()
    k = 0.5522847498
    path.moveTo(x + r, y)
    path.lineTo(x + w - r, y)
    path.curveTo(x + w - r + k * r, y, x + w, y + r - k * r, x + w, y + r)
    path.lineTo(x + w, y + h - r)
    path.curveTo(x + w, y + h - r + k * r, x + w - r + k * r, y + h, x + w - r, y + h)
    path.lineTo(x + r, y + h)
    path.curveTo(x + r - k * r, y + h, x, y + h - r + k * r, x, y + h - r)
    path.lineTo(x, y + r)
    path.curveTo(x, y + r - k * r, x + r - k * r, y, x + r, y)
    path.close()
    return path


def background(c: canvas.Canvas) -> None:
    set_fill(c, DEEP_BLACK)
    c.rect(0, 0, MEDIA_W, MEDIA_H, stroke=0, fill=1)
    set_fill(c, RICH_BLACK)
    c.rect(BLEED - 1 * mm, BLEED - 1 * mm, TRIM_W + 2 * mm, TRIM_H + 2 * mm, stroke=0, fill=1)
    set_stroke(c, (0.40, 0.35, 0.26, 0.82), 0.12)
    for i in range(9):
        y = BLEED + (5 + i * 5.2) * mm
        c.line(BLEED + 6 * mm, y, BLEED + 84 * mm, y + math.sin(i) * 0.5 * mm)
    for i in range(12):
        set_stroke(c, (0.64, 0.52, 0.36, 0.88), 0.08)
        c.circle(BLEED + (8 + i * 7.1) * mm, BLEED + (7 + (i * 11) % 37) * mm, 0.18 * mm, stroke=1, fill=0)


def border(c: canvas.Canvas) -> None:
    x = BLEED + 1.6 * mm
    y = BLEED + 1.6 * mm
    w = TRIM_W - 3.2 * mm
    h = TRIM_H - 3.2 * mm
    set_stroke(c, GOLD_DARK, 0.45)
    c.drawPath(rounded_card_path(c, x, y, w, h, 3.0 * mm), stroke=1, fill=0)
    set_stroke(c, GOLD_LIGHT, 0.16)
    c.drawPath(rounded_card_path(c, x + 0.45 * mm, y + 0.45 * mm, w - 0.9 * mm, h - 0.9 * mm, 2.5 * mm), stroke=1, fill=0)
    for px, py in (
        (x + 0.2 * mm, y + 0.2 * mm),
        (x + w - 0.2 * mm, y + 0.2 * mm),
        (x + 0.2 * mm, y + h - 0.2 * mm),
        (x + w - 0.2 * mm, y + h - 0.2 * mm),
    ):
        set_fill(c, GOLD)
        c.circle(px, py, 0.23 * mm, stroke=0, fill=1)


def star_points(cx: float, cy: float, outer: float, inner: float, points: int = 9) -> list[tuple[float, float]]:
    result = []
    for i in range(points * 2):
        radius = outer if i % 2 == 0 else inner
        angle = math.pi / 2 + i * math.pi / points
        result.append((cx + math.cos(angle) * radius, cy + math.sin(angle) * radius))
    return result


def polygon(c: canvas.Canvas, pts: Iterable[tuple[float, float]], fill: tuple[float, float, float, float], stroke=None, width=0.2) -> None:
    pts = list(pts)
    path = c.beginPath()
    path.moveTo(*pts[0])
    for x, y in pts[1:]:
        path.lineTo(x, y)
    path.close()
    set_fill(c, fill)
    if stroke:
        set_stroke(c, stroke, width)
        c.drawPath(path, stroke=1, fill=1)
    else:
        c.drawPath(path, stroke=0, fill=1)


def draw_nine_point_star(c: canvas.Canvas, cx: float, cy: float, outer: float) -> None:
    polygon(c, star_points(cx, cy, outer, outer * 0.38, 9), GOLD_LIGHT, GOLD_DARK, 0.18)
    polygon(c, star_points(cx, cy, outer * 0.66, outer * 0.24, 9), GOLD, COPPER, 0.14)
    polygon(c, star_points(cx, cy, outer * 0.36, outer * 0.14, 9), WHITE, GOLD_LIGHT, 0.08)


def draw_circuit_corner(c: canvas.Canvas, x: float, y: float, flip_x: int = 1, flip_y: int = 1) -> None:
    traces = [
        [(0, 0), (8, 0), (11, 3), (18, 3)],
        [(0, 4), (5, 4), (8, 7), (18, 7), (22, 11)],
        [(2, 9), (10, 9), (12, 13), (23, 13)],
        [(6, 16), (17, 16), (21, 20), (28, 20)],
        [(13, 0), (17, -4), (27, -4)],
    ]
    for index, trace in enumerate(traces):
        set_stroke(c, GOLD_DARK if index % 2 else COPPER, 0.26)
        path = c.beginPath()
        sx, sy = trace[0]
        path.moveTo(x + flip_x * sx * mm, y + flip_y * sy * mm)
        for tx, ty in trace[1:]:
            path.lineTo(x + flip_x * tx * mm, y + flip_y * ty * mm)
        c.drawPath(path, stroke=1, fill=0)
        for tx, ty in (trace[0], trace[-1]):
            set_fill(c, GOLD)
            c.circle(x + flip_x * tx * mm, y + flip_y * ty * mm, 0.36 * mm, stroke=0, fill=1)


def draw_balance(c: canvas.Canvas, cx: float, cy: float, scale: float) -> None:
    set_stroke(c, GOLD, 0.42 * scale)
    c.line(cx - 13 * scale, cy + 1 * scale, cx + 13 * scale, cy + 1 * scale)
    c.line(cx, cy + 1 * scale, cx, cy - 9 * scale)
    c.line(cx - 7 * scale, cy - 9 * scale, cx + 7 * scale, cy - 9 * scale)
    for side in (-1, 1):
        arm = cx + side * 10 * scale
        c.line(arm, cy + 1 * scale, arm - side * 4 * scale, cy - 7 * scale)
        c.line(arm, cy + 1 * scale, arm + side * 4 * scale, cy - 7 * scale)
        path = c.beginPath()
        path.moveTo(arm - side * 6.5 * scale, cy - 7 * scale)
        path.curveTo(arm - side * 3.5 * scale, cy - 10 * scale, arm + side * 3.5 * scale, cy - 10 * scale, arm + side * 6.5 * scale, cy - 7 * scale)
        c.drawPath(path, stroke=1, fill=0)


def draw_logo_scales(c: canvas.Canvas, cx: float, cy: float, scale: float) -> None:
    set_stroke(c, GOLD_LIGHT, 0.72 * scale)
    left_arm = c.beginPath()
    left_arm.moveTo(cx - 1.0 * scale, cy + 7.6 * scale)
    left_arm.curveTo(cx - 6.2 * scale, cy + 13.1 * scale, cx - 13.9 * scale, cy + 8.7 * scale, cx - 18.4 * scale, cy + 4.3 * scale)
    c.drawPath(left_arm, stroke=1, fill=0)
    right_arm = c.beginPath()
    right_arm.moveTo(cx + 1.0 * scale, cy + 7.6 * scale)
    right_arm.curveTo(cx + 6.2 * scale, cy + 13.1 * scale, cx + 13.9 * scale, cy + 8.7 * scale, cx + 18.4 * scale, cy + 4.3 * scale)
    c.drawPath(right_arm, stroke=1, fill=0)

    set_stroke(c, GOLD_DARK, 0.28 * scale)
    c.line(cx - 17.9 * scale, cy + 4.1 * scale, cx + 17.9 * scale, cy + 4.1 * scale)
    for side in (-1, 1):
        node_x = cx + side * 18.3 * scale
        node_y = cy + 4.3 * scale
        set_fill(c, GOLD_LIGHT)
        set_stroke(c, GOLD_DARK, 0.28 * scale)
        c.circle(node_x, node_y, 1.6 * scale, stroke=1, fill=1)
        set_stroke(c, GOLD, 0.32 * scale)
        c.line(node_x, node_y - 1.0 * scale, node_x, cy - 8.4 * scale)
        c.line(node_x, node_y - 1.0 * scale, node_x - side * 4.9 * scale, cy - 9.8 * scale)
        c.line(node_x, node_y - 1.0 * scale, node_x + side * 4.9 * scale, cy - 9.8 * scale)
        bowl = c.beginPath()
        bowl.moveTo(node_x - side * 7.3 * scale, cy - 9.5 * scale)
        bowl.curveTo(node_x - side * 4.2 * scale, cy - 12.8 * scale, node_x + side * 4.2 * scale, cy - 12.8 * scale, node_x + side * 7.3 * scale, cy - 9.5 * scale)
        c.drawPath(bowl, stroke=1, fill=0)
        set_stroke(c, COPPER, 0.20 * scale)
        c.line(node_x - side * 6.0 * scale, cy - 10.3 * scale, node_x + side * 6.0 * scale, cy - 10.3 * scale)


def draw_logo_mark(c: canvas.Canvas, fonts: dict[str, OutlineFont], cx: float, cy: float, scale: float, with_wordmark: bool) -> None:
    digit_font = fonts["serif"]
    word_font = fonts["serif_bold"]
    set_stroke(c, GOLD_DARK, 0.52 * scale)
    c.circle(cx, cy, 18.8 * scale, stroke=1, fill=0)
    set_stroke(c, GOLD, 0.22 * scale)
    c.circle(cx, cy, 15.8 * scale, stroke=1, fill=0)
    set_stroke(c, COPPER, 0.12 * scale)
    c.circle(cx, cy, 12.0 * scale, stroke=1, fill=0)
    for i in range(18):
        angle = i * math.pi / 9
        r1 = 5.4 * scale
        r2 = 18.1 * scale
        set_stroke(c, GOLD_DARK if i % 2 else COPPER, 0.10 * scale)
        c.line(cx + math.cos(angle) * r1, cy + math.sin(angle) * r1, cx + math.cos(angle) * r2, cy + math.sin(angle) * r2)

    draw_logo_scales(c, cx, cy, scale)
    draw_nine_point_star(c, cx, cy + 20.9 * scale, 5.1 * scale)

    size = 33.6 * scale
    baseline = cy - 15.6 * scale
    hscale = 0.76
    stroke_width = 0.42 * scale
    digit_w = digit_font.text_width("9", size, horizontal_scale=hscale)
    left_x = cx - 1.6 * scale - digit_w
    right_edge = cx + 1.6 * scale + digit_w
    digit_font.draw(
        c,
        "9",
        left_x,
        baseline - 0.35 * scale,
        size,
        GOLD_DARK,
        horizontal_scale=hscale,
    )
    digit_font.draw_mirrored(
        c,
        "9",
        right_edge,
        baseline - 0.35 * scale,
        size,
        GOLD_DARK,
        horizontal_scale=hscale,
    )
    digit_font.draw(
        c,
        "9",
        left_x,
        baseline,
        size,
        GOLD_LIGHT,
        horizontal_scale=hscale,
        stroke=GOLD_DARK,
        stroke_width=stroke_width,
    )
    digit_font.draw_mirrored(
        c,
        "9",
        right_edge,
        baseline,
        size,
        GOLD_LIGHT,
        horizontal_scale=hscale,
        stroke=GOLD_DARK,
        stroke_width=stroke_width,
    )

    pillar = c.beginPath()
    pillar.moveTo(cx - 1.55 * scale, cy - 18.7 * scale)
    pillar.lineTo(cx + 1.55 * scale, cy - 18.7 * scale)
    pillar.lineTo(cx + 1.12 * scale, cy + 7.2 * scale)
    pillar.lineTo(cx + 3.35 * scale, cy + 7.2 * scale)
    pillar.lineTo(cx, cy + 11.6 * scale)
    pillar.lineTo(cx - 3.35 * scale, cy + 7.2 * scale)
    pillar.lineTo(cx - 1.12 * scale, cy + 7.2 * scale)
    pillar.close()
    set_fill(c, GOLD_LIGHT)
    set_stroke(c, GOLD_DARK, 0.32 * scale)
    c.drawPath(pillar, stroke=1, fill=1)
    set_stroke(c, WHITE, 0.10 * scale)
    c.line(cx - 0.45 * scale, cy - 16.7 * scale, cx - 0.30 * scale, cy + 6.6 * scale)
    set_stroke(c, GOLD_DARK, 0.26 * scale)
    c.line(cx - 4.4 * scale, cy - 18.9 * scale, cx + 4.4 * scale, cy - 18.9 * scale)
    if with_wordmark:
        word_font.draw(
            c,
            "JUS 9",
            cx,
            cy - 36.0 * scale,
            18.8 * scale,
            GOLD_LIGHT,
            tracking=1.0 * scale,
            centered=True,
            stroke=GOLD_DARK,
            stroke_width=0.18 * scale,
        )


def small_caps(c: canvas.Canvas, font: OutlineFont, text: str, cx: float, y: float, size: float, tracking: float, color=GOLD) -> None:
    font.draw(c, text, cx, y, size, color, tracking=tracking, centered=True)


def quiet_panel(c: canvas.Canvas, x: float, y: float, w: float, h: float) -> None:
    set_fill(c, RICH_BLACK)
    c.rect(x, y, w, h, stroke=0, fill=1)


def front(c: canvas.Canvas, fonts: dict[str, OutlineFont]) -> None:
    background(c)
    border(c)
    draw_circuit_corner(c, BLEED + 6 * mm, BLEED + 4 * mm, 1, 1)
    draw_circuit_corner(c, BLEED + 88 * mm, BLEED + 47 * mm, -1, -1)
    cx = BLEED + TRIM_W / 2
    draw_logo_mark(c, fonts, cx, BLEED + 30.2 * mm, 1.02, True)
    small_caps(c, fonts["sans"], "TECNOLOGIA JURÍDICA", cx, BLEED + 9.55 * mm, 6.4, 2.35, GOLD)
    set_stroke(c, COPPER, 0.25)
    c.line(cx - 18 * mm, BLEED + 8.7 * mm, cx - 10 * mm, BLEED + 8.7 * mm)
    c.line(cx + 10 * mm, BLEED + 8.7 * mm, cx + 18 * mm, BLEED + 8.7 * mm)
    small_caps(c, fonts["sans"], "certificação FSC", cx, BLEED + 5.95 * mm, 3.9, 0.42, GOLD_DARK)


def icon_circle(c: canvas.Canvas, x: float, y: float, label: str, fonts: dict[str, OutlineFont]) -> None:
    set_stroke(c, GOLD, 0.52)
    c.circle(x, y, 2.9 * mm, stroke=1, fill=0)
    if label == "phone":
        set_stroke(c, GOLD, 0.55)
        path = c.beginPath()
        path.moveTo(x - 1.2 * mm, y + 1.4 * mm)
        path.curveTo(x - 2.2 * mm, y + 0.3 * mm, x - 1.2 * mm, y - 1.7 * mm, x + 1.3 * mm, y - 1.8 * mm)
        c.drawPath(path, stroke=1, fill=0)
        c.rect(x - 1.7 * mm, y + 1.0 * mm, 0.9 * mm, 1.2 * mm, stroke=1, fill=0)
        c.rect(x + 0.9 * mm, y - 2.0 * mm, 0.9 * mm, 1.2 * mm, stroke=1, fill=0)
    elif label == "mail":
        set_stroke(c, GOLD, 0.45)
        c.rect(x - 1.7 * mm, y - 1.15 * mm, 3.4 * mm, 2.3 * mm, stroke=1, fill=0)
        c.line(x - 1.7 * mm, y + 1.15 * mm, x, y - 0.25 * mm)
        c.line(x + 1.7 * mm, y + 1.15 * mm, x, y - 0.25 * mm)
    elif label == "web":
        set_stroke(c, GOLD, 0.38)
        c.circle(x, y, 1.65 * mm, stroke=1, fill=0)
        c.line(x - 1.65 * mm, y, x + 1.65 * mm, y)
        c.line(x, y - 1.65 * mm, x, y + 1.65 * mm)
        c.ellipse(x - 0.85 * mm, y - 1.65 * mm, x + 0.85 * mm, y + 1.65 * mm, stroke=1, fill=0)
    elif label == "in":
        fonts["sans_bold"].draw(c, "in", x - 1.35 * mm, y - 1.25 * mm, 5.2, GOLD, horizontal_scale=0.95)


def back(c: canvas.Canvas, fonts: dict[str, OutlineFont]) -> None:
    background(c)
    draw_circuit_corner(c, BLEED + 5 * mm, BLEED + 5 * mm, 1, 1)
    draw_circuit_corner(c, BLEED + 89 * mm, BLEED + 49 * mm, -1, -1)
    quiet_panel(c, BLEED + 40.2 * mm, BLEED + 29.0 * mm, 48.4 * mm, 13.4 * mm)
    quiet_panel(c, BLEED + 48.2 * mm, BLEED + 6.4 * mm, 39.4 * mm, 23.0 * mm)

    draw_logo_mark(c, fonts, BLEED + 24.5 * mm, BLEED + 30.4 * mm, 0.62, True)
    fonts["sans"].draw(c, "TECNOLOGIA JURÍDICA", BLEED + 24.5 * mm, BLEED + 8.9 * mm, 4.65, GOLD, tracking=1.05, horizontal_scale=0.82, centered=True)

    set_stroke(c, GOLD_DARK, 0.55)
    c.line(BLEED + 37.7 * mm, BLEED + 7.5 * mm, BLEED + 37.7 * mm, BLEED + 42.5 * mm)
    set_fill(c, GOLD)
    c.circle(BLEED + 37.7 * mm, BLEED + 25 * mm, 0.43 * mm, stroke=0, fill=1)

    left = BLEED + 42.6 * mm
    fonts["serif_bold"].draw(c, "Clovis Mariano da Costa / Aeon Primevo", left, BLEED + 36.7 * mm, 7.65, GOLD, horizontal_scale=0.74)
    fonts["serif"].draw(c, "Fundador — Jus 9 Tecnologia Jurídica", left, BLEED + 32.9 * mm, 5.9, MUTED_WHITE, horizontal_scale=0.82)

    rows = [
        ("phone", "+55 48 99908 2726"),
        ("mail", "clovis@jus9tecnologia.com.br"),
        ("web", "www.jus9tecnologia.com.br"),
        ("in", "linkedin.com/company/jus-9-tecnologia-juridica"),
    ]
    y = BLEED + 26.1 * mm
    for icon, text in rows:
        icon_circle(c, BLEED + 44.2 * mm, y + 0.8 * mm, icon, fonts)
        hscale = 0.66 if icon == "in" else 0.82
        size = 6.15 if icon != "in" else 5.5
        fonts["serif"].draw(c, text, BLEED + 49.2 * mm, y - 0.6 * mm, size, WHITE, horizontal_scale=hscale)
        y -= 7.35 * mm


def add_output_intent(pdf_path: Path) -> None:
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    writer._header = b"%PDF-1.4"

    icc_stream = DecodedStreamObject()
    icc_stream.set_data(ICC_PROFILE.read_bytes())
    icc_stream.update({NameObject("/N"): FloatObject(4)})
    icc_ref = writer._add_object(icc_stream)
    output_intent = DictionaryObject(
        {
            NameObject("/Type"): NameObject("/OutputIntent"),
            NameObject("/S"): NameObject("/GTS_PDFX"),
            NameObject("/OutputConditionIdentifier"): TextStringObject("U.S. Web Coated (SWOP) v2"),
            NameObject("/Info"): TextStringObject("CMYK output intent: U.S. Web Coated (SWOP) v2"),
            NameObject("/RegistryName"): TextStringObject("http://www.color.org"),
            NameObject("/DestOutputProfile"): icc_ref,
        }
    )
    writer.root_object.update({NameObject("/OutputIntents"): ArrayObject([writer._add_object(output_intent)])})
    for page in writer.pages:
        page[NameObject("/TrimBox")] = RectangleObject(
            [FloatObject(BLEED), FloatObject(BLEED), FloatObject(BLEED + TRIM_W), FloatObject(BLEED + TRIM_H)]
        )
        page[NameObject("/BleedBox")] = RectangleObject(
            [FloatObject(0), FloatObject(0), FloatObject(MEDIA_W), FloatObject(MEDIA_H)]
        )
    writer.add_metadata(
        {
            "/Title": pdf_path.stem,
            "/Creator": "Codex vector card generator",
            "/Subject": "Arte vetorial CMYK com sangria 3 mm e textos em curvas",
            "/GTS_PDFXVersion": "PDF/X-1a:2001",
            "/GTS_PDFXConformance": "PDF/X-1a:2001",
        }
    )
    tmp = pdf_path.with_suffix(".tmp.pdf")
    with tmp.open("wb") as handle:
        writer.write(handle)
    tmp.replace(pdf_path)


def write_pdf(path: Path, page_fn, fonts: dict[str, OutlineFont]) -> None:
    c = canvas.Canvas(str(path), pagesize=(MEDIA_W, MEDIA_H), pageCompression=1, pdfVersion=(1, 4))
    c.setTitle(path.stem)
    page_fn(c, fonts)
    c.showPage()
    c.save()
    add_output_intent(path)


def preview(path: Path) -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    with fitz.open(path) as doc:
        pix = doc[0].get_pixmap(dpi=300, alpha=False)
        pix.save(PREVIEW_DIR / f"{path.stem}_preview.png")


def validate(path: Path) -> None:
    reader = PdfReader(path)
    assert len(reader.pages) == 1
    root = reader.trailer["/Root"]
    assert len(root.get("/OutputIntents", [])) == 1
    with fitz.open(path) as doc:
        page = doc[0]
        assert abs(page.rect.width * 25.4 / 72 - 96.0) < 0.02
        assert abs(page.rect.height * 25.4 / 72 - 56.0) < 0.02
        assert not page.get_images(full=True)
        text = page.get_text().strip()
        assert text == "", "Text should be converted to outlines, not live fonts"


def main() -> None:
    for required in (ICC_PROFILE, FONT_SERIF, FONT_SERIF_BOLD, FONT_SANS, FONT_SANS_BOLD):
        if not required.exists():
            raise FileNotFoundError(required)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fonts = {
        "serif": OutlineFont(FONT_SERIF),
        "serif_bold": OutlineFont(FONT_SERIF_BOLD),
        "sans": OutlineFont(FONT_SANS),
        "sans_bold": OutlineFont(FONT_SANS_BOLD),
    }
    front_pdf = OUT_DIR / "Jus9_Cartao_Frente_Redesenho_Vetorial_CMYK.pdf"
    back_pdf = OUT_DIR / "Jus9_Cartao_Verso_Redesenho_Vetorial_CMYK.pdf"
    write_pdf(front_pdf, front, fonts)
    write_pdf(back_pdf, back, fonts)
    for pdf in (front_pdf, back_pdf):
        preview(pdf)
        validate(pdf)
        print(pdf)


if __name__ == "__main__":
    main()
