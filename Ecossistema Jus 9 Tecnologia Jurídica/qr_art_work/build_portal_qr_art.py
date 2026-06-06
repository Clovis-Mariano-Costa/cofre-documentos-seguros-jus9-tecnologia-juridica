from __future__ import annotations

import math
import re
from pathlib import Path

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


TRIM_W_MM = 100.0
TRIM_H_MM = 150.0
BLEED_MM = 3.0
MEDIA_W = (TRIM_W_MM + 2 * BLEED_MM) * mm
MEDIA_H = (TRIM_H_MM + 2 * BLEED_MM) * mm
BLEED = BLEED_MM * mm
TRIM_W = TRIM_W_MM * mm
TRIM_H = TRIM_H_MM * mm

WORK = Path(__file__).resolve().parent
OUT_DIR = Path.home() / "Downloads" / "Arte QR Portal Jus9 10x15 CMYK"
PREVIEW_DIR = OUT_DIR / "previews"
QR_SVG = WORK / "portal-jus9.svg"
ICC_PROFILE = Path(r"C:\Windows\System32\spool\drivers\color\RSWOP.icm")

FONT_SERIF = Path(r"C:\Windows\Fonts\georgia.ttf")
FONT_SERIF_BOLD = Path(r"C:\Windows\Fonts\georgiab.ttf")
FONT_SANS = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_SANS_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")

RICH_NAVY = (0.88, 0.70, 0.46, 0.92)
DEEP_NAVY = (0.94, 0.76, 0.50, 0.96)
PANEL_NAVY = (0.90, 0.72, 0.50, 0.90)
QR_DARK = (0.84, 0.72, 0.58, 0.88)
GOLD = (0.06, 0.20, 0.96, 0.02)
GOLD_LIGHT = (0.00, 0.08, 0.54, 0.00)
GOLD_DARK = (0.14, 0.34, 0.90, 0.16)
COPPER = (0.08, 0.54, 0.92, 0.08)
WHITE = (0.00, 0.00, 0.00, 0.00)
WARM_WHITE = (0.02, 0.02, 0.08, 0.00)
MUTED_LINE = (0.48, 0.38, 0.24, 0.76)


class OutlineFont:
    def __init__(self, path: Path):
        self.font = TTFont(path)
        self.glyph_set = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap()
        self.hmtx = self.font["hmtx"].metrics
        self.units_per_em = self.font["head"].unitsPerEm
        self.space_width = self.hmtx.get("space", (self.units_per_em // 3, 0))[0]

    def glyph_name(self, char: str) -> str:
        return self.cmap.get(ord(char), ".notdef")

    def text_width(self, text: str, size: float, tracking: float = 0.0, horizontal_scale: float = 1.0) -> float:
        scale = size / self.units_per_em * horizontal_scale
        total = 0.0
        for index, char in enumerate(text):
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
                elif operator == "curveTo":
                    p1, p2, p3 = args
                    current_point = (cursor + p3[0] * scale * horizontal_scale, y + p3[1] * scale)
                    path.curveTo(
                        cursor + p1[0] * scale * horizontal_scale,
                        y + p1[1] * scale,
                        cursor + p2[0] * scale * horizontal_scale,
                        y + p2[1] * scale,
                        *current_point,
                    )
                elif operator == "qCurveTo":
                    if current_point is None:
                        continue
                    points = [p for p in args if p is not None]
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
                            end_x = cursor + ex * scale * horizontal_scale
                            end_y = y + ey * scale
                            control_x = cursor + qx * scale * horizontal_scale
                            control_y = y + qy * scale
                            cx1 = start_x + (2 / 3) * (control_x - start_x)
                            cy1 = start_y + (2 / 3) * (control_y - start_y)
                            cx2 = end_x + (2 / 3) * (control_x - end_x)
                            cy2 = end_y + (2 / 3) * (control_y - end_y)
                            path.curveTo(cx1, cy1, cx2, cy2, end_x, end_y)
                            start_x, start_y = end_x, end_y
                        current_point = (start_x, start_y)
                elif operator == "closePath":
                    path.close()
                    current_point = None
            c.drawPath(path, stroke=1 if stroke else 0, fill=1)
            advance = self.hmtx.get(glyph_name, (self.space_width, 0))[0]
            cursor += advance * scale * horizontal_scale
            if index != len(text) - 1:
                cursor += tracking


def set_fill(c: canvas.Canvas, color: tuple[float, float, float, float]) -> None:
    c.setFillColorCMYK(*color)


def set_stroke(c: canvas.Canvas, color: tuple[float, float, float, float], width: float) -> None:
    c.setStrokeColorCMYK(*color)
    c.setLineWidth(width)


def rounded_path(c: canvas.Canvas, x: float, y: float, w: float, h: float, r: float):
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


def parse_qr_segments(svg_path: Path) -> list[tuple[float, float, float]]:
    svg = svg_path.read_text(encoding="utf-8")
    match = re.search(r"<path stroke=\"#[0-9a-fA-F]+\" d=\"([^\"]+)\"", svg)
    if not match:
        raise ValueError("Could not find QR stroke path")
    tokens = re.findall(r"[Mmhv]|-?\d+(?:\.\d+)?", match.group(1))
    x = y = 0.0
    index = 0
    segments: list[tuple[float, float, float]] = []
    while index < len(tokens):
        token = tokens[index]
        if token == "M":
            x = float(tokens[index + 1])
            y = float(tokens[index + 2])
            index += 3
        elif token == "m":
            x += float(tokens[index + 1])
            y += float(tokens[index + 2])
            index += 3
        elif token == "h":
            length = float(tokens[index + 1])
            segments.append((x, y - 0.5, length))
            x += length
            index += 2
        elif token == "H":
            new_x = float(tokens[index + 1])
            segments.append((min(x, new_x), y - 0.5, abs(new_x - x)))
            x = new_x
            index += 2
        else:
            raise ValueError(f"Unexpected SVG token: {token}")
    return segments


def draw_qr(c: canvas.Canvas, x: float, y: float, size: float) -> None:
    module = size / 37.0
    set_fill(c, WHITE)
    c.rect(x, y, size, size, stroke=0, fill=1)
    set_fill(c, QR_DARK)
    for sx, sy, length in parse_qr_segments(QR_SVG):
        c.rect(x + sx * module, y + (37.0 - sy - 1.0) * module, length * module, module, stroke=0, fill=1)


def circuit_side(c: canvas.Canvas, x: float, y: float, mirror: int) -> None:
    traces = [
        [(0, 0), (7, 7), (7, 18), (12, 23), (12, 34)],
        [(2, 18), (9, 25), (9, 42), (15, 48), (15, 58)],
        [(0, 41), (6, 47), (6, 72), (13, 79), (13, 92)],
        [(3, 85), (10, 92), (10, 108), (16, 114)],
        [(1, 113), (8, 120), (8, 132)],
    ]
    for i, trace in enumerate(traces):
        set_stroke(c, GOLD_DARK if i % 2 else COPPER, 0.36)
        p = c.beginPath()
        sx, sy = trace[0]
        p.moveTo(x + mirror * sx * mm, y + sy * mm)
        for tx, ty in trace[1:]:
            p.lineTo(x + mirror * tx * mm, y + ty * mm)
        c.drawPath(p, stroke=1, fill=0)
        for tx, ty in (trace[0], trace[-1]):
            set_fill(c, GOLD)
            c.circle(x + mirror * tx * mm, y + ty * mm, 0.55 * mm, stroke=0, fill=1)


def draw_icon(c: canvas.Canvas, x: float, y: float, kind: str, fonts: dict[str, OutlineFont]) -> None:
    set_stroke(c, GOLD, 0.62)
    c.circle(x, y, 4.7 * mm, stroke=1, fill=0)
    if kind == "web":
        c.circle(x, y, 2.9 * mm, stroke=1, fill=0)
        c.line(x - 2.9 * mm, y, x + 2.9 * mm, y)
        c.line(x, y - 2.9 * mm, x, y + 2.9 * mm)
        c.ellipse(x - 1.35 * mm, y - 2.9 * mm, x + 1.35 * mm, y + 2.9 * mm, stroke=1, fill=0)
    elif kind == "phone":
        p = c.beginPath()
        p.moveTo(x - 2.1 * mm, y + 2.6 * mm)
        p.curveTo(x - 4.0 * mm, y + 0.1 * mm, x - 1.2 * mm, y - 3.5 * mm, x + 3.0 * mm, y - 2.6 * mm)
        c.drawPath(p, stroke=1, fill=0)
        c.rect(x - 2.7 * mm, y + 1.9 * mm, 1.4 * mm, 1.7 * mm, stroke=1, fill=0)
        c.rect(x + 2.1 * mm, y - 3.2 * mm, 1.4 * mm, 1.7 * mm, stroke=1, fill=0)
    elif kind == "in":
        fonts["sans_bold"].draw(c, "in", x - 2.5 * mm, y - 2.1 * mm, 10.6, GOLD)


def background(c: canvas.Canvas) -> None:
    set_fill(c, DEEP_NAVY)
    c.rect(0, 0, MEDIA_W, MEDIA_H, stroke=0, fill=1)
    set_fill(c, RICH_NAVY)
    c.rect(BLEED, BLEED, TRIM_W, TRIM_H, stroke=0, fill=1)
    set_fill(c, PANEL_NAVY)
    c.rect(BLEED + 2 * mm, BLEED + 2 * mm, TRIM_W - 4 * mm, TRIM_H - 4 * mm, stroke=0, fill=1)
    for i in range(42):
        set_stroke(c, MUTED_LINE, 0.08)
        yy = BLEED + (8 + i * 3.35) * mm
        c.line(BLEED + 9 * mm, yy, BLEED + 91 * mm, yy + math.sin(i * 0.7) * 0.18 * mm)
    for i in range(24):
        set_fill(c, (0.30, 0.40, 0.24, 0.78))
        c.circle(BLEED + (10 + (i * 13) % 80) * mm, BLEED + (18 + (i * 29) % 120) * mm, 0.22 * mm, stroke=0, fill=1)


def border(c: canvas.Canvas) -> None:
    x = BLEED + 3.0 * mm
    y = BLEED + 3.0 * mm
    w = TRIM_W - 6.0 * mm
    h = TRIM_H - 6.0 * mm
    set_stroke(c, GOLD, 0.72)
    c.drawPath(rounded_path(c, x, y, w, h, 5.2 * mm), stroke=1, fill=0)
    set_stroke(c, GOLD_DARK, 0.34)
    c.drawPath(rounded_path(c, x + 1.1 * mm, y + 1.1 * mm, w - 2.2 * mm, h - 2.2 * mm, 4.2 * mm), stroke=1, fill=0)
    for px, py in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
        set_fill(c, GOLD)
        c.circle(px, py, 0.45 * mm, stroke=0, fill=1)
    set_fill(c, GOLD)
    diamond = c.beginPath()
    diamond.moveTo(BLEED + 50 * mm, y - 0.6 * mm)
    diamond.lineTo(BLEED + 52.0 * mm, y + 1.4 * mm)
    diamond.lineTo(BLEED + 50 * mm, y + 3.4 * mm)
    diamond.lineTo(BLEED + 48.0 * mm, y + 1.4 * mm)
    diamond.close()
    c.drawPath(diamond, stroke=0, fill=1)


def draw_art(c: canvas.Canvas, fonts: dict[str, OutlineFont]) -> None:
    background(c)
    border(c)
    circuit_side(c, BLEED + 8.0 * mm, BLEED + 22 * mm, 1)
    circuit_side(c, BLEED + 92.0 * mm, BLEED + 22 * mm, -1)

    cx = BLEED + TRIM_W / 2
    fonts["serif_bold"].draw(c, "JUS 9", cx, BLEED + 124.2 * mm, 38, GOLD_LIGHT, tracking=4.0, horizontal_scale=1.0, centered=True, stroke=GOLD_DARK, stroke_width=0.22)
    set_stroke(c, GOLD, 0.42)
    c.line(BLEED + 17 * mm, BLEED + 116.7 * mm, BLEED + 25 * mm, BLEED + 116.7 * mm)
    c.line(BLEED + 75 * mm, BLEED + 116.7 * mm, BLEED + 83 * mm, BLEED + 116.7 * mm)
    fonts["sans"].draw(c, "TECNOLOGIA JURÍDICA", cx, BLEED + 114.4 * mm, 9.8, GOLD, tracking=2.05, horizontal_scale=0.88, centered=True)

    qr_box_w = 58.0 * mm
    qr_box_h = 58.0 * mm
    qr_box_x = BLEED + (TRIM_W_MM * mm - qr_box_w) / 2
    qr_box_y = BLEED + 49.5 * mm
    set_fill(c, WHITE)
    c.drawPath(rounded_path(c, qr_box_x, qr_box_y, qr_box_w, qr_box_h, 3.5 * mm), stroke=0, fill=1)
    set_stroke(c, GOLD, 0.78)
    c.drawPath(rounded_path(c, qr_box_x, qr_box_y, qr_box_w, qr_box_h, 3.5 * mm), stroke=1, fill=0)
    set_stroke(c, GOLD_DARK, 0.28)
    c.drawPath(rounded_path(c, qr_box_x + 1.1 * mm, qr_box_y + 1.1 * mm, qr_box_w - 2.2 * mm, qr_box_h - 2.2 * mm, 2.5 * mm), stroke=1, fill=0)
    draw_qr(c, qr_box_x + 4.6 * mm, qr_box_y + 4.6 * mm, qr_box_w - 9.2 * mm)

    set_stroke(c, GOLD_DARK, 0.25)
    c.line(BLEED + 31.0 * mm, BLEED + 48.8 * mm, BLEED + 47.5 * mm, BLEED + 48.8 * mm)
    c.line(BLEED + 52.5 * mm, BLEED + 48.8 * mm, BLEED + 69.0 * mm, BLEED + 48.8 * mm)
    set_fill(c, GOLD)
    d = c.beginPath()
    d.moveTo(cx, BLEED + 50.4 * mm)
    d.lineTo(cx + 1.7 * mm, BLEED + 48.8 * mm)
    d.lineTo(cx, BLEED + 47.1 * mm)
    d.lineTo(cx - 1.7 * mm, BLEED + 48.8 * mm)
    d.close()
    c.drawPath(d, stroke=0, fill=1)
    fonts["serif_bold"].draw(c, "Acesse o portal da Jus 9", cx, BLEED + 40.8 * mm, 15.6, WARM_WHITE, horizontal_scale=0.94, centered=True, stroke=(0.42, 0.35, 0.28, 0.88), stroke_width=0.10)

    rows = [
        ("web", "www.jus9tecnologia.com.br", 29.2),
        ("phone", "+55 48 99908 2726", 18.7),
        ("in", "linkedin.com/company/jus-9-tecnologia-juridica", 8.2),
    ]
    for kind, text, y_mm in rows:
        y = BLEED + y_mm * mm
        draw_icon(c, BLEED + 16.8 * mm, y + 1.1 * mm, kind, fonts)
        set_stroke(c, GOLD, 0.35)
        c.line(BLEED + 26.8 * mm, y - 3.8 * mm, BLEED + 26.8 * mm, y + 4.0 * mm)
        size = 10.0 if kind != "in" else 7.6
        hscale = 0.93 if kind != "in" else 0.74
        fonts["sans"].draw(c, text, BLEED + 30.2 * mm, y - 1.7 * mm, size, WHITE, horizontal_scale=hscale)
        if kind != "in":
            set_stroke(c, GOLD_DARK, 0.22)
            c.line(BLEED + 10.0 * mm, y - 6.6 * mm, BLEED + 90.0 * mm, y - 6.6 * mm)


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
    page = writer.pages[0]
    page[NameObject("/TrimBox")] = RectangleObject([FloatObject(BLEED), FloatObject(BLEED), FloatObject(BLEED + TRIM_W), FloatObject(BLEED + TRIM_H)])
    page[NameObject("/BleedBox")] = RectangleObject([FloatObject(0), FloatObject(0), FloatObject(MEDIA_W), FloatObject(MEDIA_H)])
    writer.add_metadata(
        {
            "/Title": "Arte QR Portal Jus 9 - 10x15 CMYK",
            "/Creator": "Codex vector PDF generator",
            "/Subject": "Arte vertical 10x15 cm em CMYK, QR vetorial e textos em curvas",
            "/GTS_PDFXVersion": "PDF/X-1a:2001",
            "/GTS_PDFXConformance": "PDF/X-1a:2001",
        }
    )
    tmp = pdf_path.with_suffix(".tmp.pdf")
    with tmp.open("wb") as handle:
        writer.write(handle)
    tmp.replace(pdf_path)


def write_pdf(path: Path, fonts: dict[str, OutlineFont]) -> None:
    c = canvas.Canvas(str(path), pagesize=(MEDIA_W, MEDIA_H), pageCompression=1, pdfVersion=(1, 4))
    c.setTitle("Arte QR Portal Jus 9 - 10x15 CMYK")
    draw_art(c, fonts)
    c.showPage()
    c.save()
    add_output_intent(path)


def preview(path: Path) -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    with fitz.open(path) as doc:
        pix = doc[0].get_pixmap(dpi=220, alpha=False)
        pix.save(PREVIEW_DIR / f"{path.stem}_preview.png")


def validate(path: Path) -> None:
    reader = PdfReader(path)
    assert len(reader.pages) == 1
    assert len(reader.trailer["/Root"].get("/OutputIntents", [])) == 1
    with fitz.open(path) as doc:
        page = doc[0]
        assert abs(page.rect.width * 25.4 / 72 - 106.0) < 0.02
        assert abs(page.rect.height * 25.4 / 72 - 156.0) < 0.02
        assert len(page.get_images(full=True)) == 0
        assert len(page.get_text()) == 0


def main() -> None:
    for required in (QR_SVG, ICC_PROFILE, FONT_SERIF, FONT_SERIF_BOLD, FONT_SANS, FONT_SANS_BOLD):
        if not required.exists():
            raise FileNotFoundError(required)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fonts = {
        "serif": OutlineFont(FONT_SERIF),
        "serif_bold": OutlineFont(FONT_SERIF_BOLD),
        "sans": OutlineFont(FONT_SANS),
        "sans_bold": OutlineFont(FONT_SANS_BOLD),
    }
    output = OUT_DIR / "Jus9_QR_Portal_10x15cm_CMYK.pdf"
    write_pdf(output, fonts)
    preview(output)
    validate(output)
    print(output)


if __name__ == "__main__":
    main()
