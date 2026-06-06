from __future__ import annotations

from pathlib import Path
from typing import Callable

import fitz
from PIL import Image, ImageDraw, ImageFilter
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    DecodedStreamObject,
    DictionaryObject,
    FloatObject,
    NameObject,
    NumberObject,
    RectangleObject,
    TextStringObject,
)
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


TRIM_WIDTH_MM = 90.0
TRIM_HEIGHT_MM = 50.0
BLEED_MM = 3.0
DPI = 600
ICC_PROFILE = Path(r"C:\Windows\System32\spool\drivers\color\RSWOP.icm")
TIMES_FONT = Path(r"C:\Windows\Fonts\times.ttf")
ARIAL_FONT = Path(r"C:\Windows\Fonts\arial.ttf")
OUT_DIR = Path(__file__).resolve().parent / "output"
ASSET_DIR = Path(__file__).resolve().parent / "generated_assets"

GOLD = (0.03, 0.16, 0.90, 0.04)
SOFT_WHITE = (0.02, 0.02, 0.07, 0.04)


def mm_from_source_x(px: float) -> float:
    return px / 1010.0 * TRIM_WIDTH_MM * mm


def mm_from_source_baseline(px_from_top: float) -> float:
    return (561.0 - px_from_top) / 561.0 * TRIM_HEIGHT_MM * mm


def extract_background(pdf_path: Path, destination: Path) -> None:
    with fitz.open(pdf_path) as document:
        image_xref = document[0].get_images(full=True)[0][0]
        extracted = document.extract_image(image_xref)
        destination.write_bytes(extracted["image"])


def patch_text_region(
    image: Image.Image,
    box: tuple[int, int, int, int],
    sample_box: tuple[int, int, int, int],
    feather_px: int = 6,
) -> None:
    left, top, right, bottom = box
    extended = (
        max(0, left - feather_px),
        max(0, top - feather_px),
        min(image.width, right + feather_px),
        min(image.height, bottom + feather_px),
    )
    width = extended[2] - extended[0]
    height = extended[3] - extended[1]
    patch = image.crop(sample_box).resize((width, height), Image.Resampling.LANCZOS)
    mask = Image.new("L", (width, height), color=0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle(
        (
            feather_px,
            feather_px,
            width - feather_px - 1,
            height - feather_px - 1,
        ),
        fill=255,
    )
    mask = mask.filter(ImageFilter.GaussianBlur(radius=feather_px / 2))
    image.paste(patch, (extended[0], extended[1]), mask)


def remove_raster_text(image: Image.Image, side: str) -> None:
    sample_boxes = {
        "front": (75, 100, 325, 175),
        "back": (375, 20, 625, 100),
    }
    boxes = {
        "front": [
            (350, 443, 663, 474),
            (435, 479, 575, 502),
        ],
        "back": [
            (142, 393, 360, 418),
            (445, 143, 952, 183),
            (445, 187, 810, 217),
            (502, 246, 690, 280),
            (502, 307, 780, 342),
            (502, 369, 782, 403),
            (502, 429, 958, 464),
        ],
    }
    for box in boxes[side]:
        patch_text_region(image, box, sample_boxes[side])


def improve_background(
    source: Path,
    destination: Path,
    bleed_mm: float,
    side: str,
) -> None:
    trim_width_px = round(TRIM_WIDTH_MM / 25.4 * DPI)
    trim_height_px = round(TRIM_HEIGHT_MM / 25.4 * DPI)
    bleed_px = round(bleed_mm / 25.4 * DPI)

    with Image.open(source) as original:
        cmyk = original.convert("CMYK")
        remove_raster_text(cmyk, side)
        sharpened = cmyk.resize(
            (trim_width_px, trim_height_px),
            Image.Resampling.LANCZOS,
        ).filter(ImageFilter.UnsharpMask(radius=0.75, percent=85, threshold=3))

    if not bleed_px:
        final_image = sharpened
    else:
        final_image = Image.new(
            "CMYK",
            (trim_width_px + 2 * bleed_px, trim_height_px + 2 * bleed_px),
        )
        final_image.paste(sharpened, (bleed_px, bleed_px))

        top = sharpened.crop((0, 0, trim_width_px, 1)).resize(
            (trim_width_px, bleed_px)
        )
        bottom = sharpened.crop((0, trim_height_px - 1, trim_width_px, trim_height_px)).resize(
            (trim_width_px, bleed_px)
        )
        left = sharpened.crop((0, 0, 1, trim_height_px)).resize(
            (bleed_px, trim_height_px)
        )
        right = sharpened.crop((trim_width_px - 1, 0, trim_width_px, trim_height_px)).resize(
            (bleed_px, trim_height_px)
        )

        final_image.paste(top, (bleed_px, 0))
        final_image.paste(bottom, (bleed_px, bleed_px + trim_height_px))
        final_image.paste(left, (0, bleed_px))
        final_image.paste(right, (bleed_px + trim_width_px, bleed_px))

        corners = {
            (0, 0): sharpened.getpixel((0, 0)),
            (bleed_px + trim_width_px, 0): sharpened.getpixel((trim_width_px - 1, 0)),
            (0, bleed_px + trim_height_px): sharpened.getpixel((0, trim_height_px - 1)),
            (bleed_px + trim_width_px, bleed_px + trim_height_px): sharpened.getpixel(
                (trim_width_px - 1, trim_height_px - 1)
            ),
        }
        for position, color in corners.items():
            final_image.paste(
                Image.new("CMYK", (bleed_px, bleed_px), color=color),
                position,
            )

    final_image.save(
        destination,
        "JPEG",
        quality=97,
        subsampling=0,
        dpi=(DPI, DPI),
    )


def set_text_color(pdf: canvas.Canvas, color: tuple[float, float, float, float]) -> None:
    pdf.setFillColorCMYK(*color)


def draw_tracked_centered(
    pdf: canvas.Canvas,
    text: str,
    font_name: str,
    font_size: float,
    center_x: float,
    baseline_y: float,
    char_space: float,
    color: tuple[float, float, float, float],
) -> None:
    width = pdfmetrics.stringWidth(text, font_name, font_size)
    width += max(0, len(text) - 1) * char_space
    text_object = pdf.beginText(center_x - width / 2.0, baseline_y)
    text_object.setFont(font_name, font_size)
    text_object.setCharSpace(char_space)
    text_object.setFillColorCMYK(*color)
    text_object.textLine(text)
    pdf.drawText(text_object)


def draw_front_overlay(pdf: canvas.Canvas, offset: float) -> None:
    draw_tracked_centered(
        pdf,
        "TECNOLOGIA JUR\u00cdDICA",
        "ArialJus9",
        5.1,
        offset + mm_from_source_x(505),
        offset + mm_from_source_baseline(466),
        1.25,
        GOLD,
    )
    draw_tracked_centered(
        pdf,
        "certifica\u00e7\u00e3o FSC",
        "ArialJus9",
        3.4,
        offset + mm_from_source_x(505),
        offset + mm_from_source_baseline(495),
        0.62,
        GOLD,
    )


def draw_back_overlay(pdf: canvas.Canvas, offset: float) -> None:
    draw_tracked_centered(
        pdf,
        "TECNOLOGIA JUR\u00cdDICA",
        "ArialJus9",
        4.1,
        offset + mm_from_source_x(251),
        offset + mm_from_source_baseline(411),
        1.05,
        GOLD,
    )

    lines = [
        ("Clovis Mariano da Costa / Aeon Primevo", 451, 176, 7.35, 82, GOLD),
        ("Fundador \u2014 Jus 9 Tecnologia Jur\u00eddica", 451, 213, 6.35, 82, SOFT_WHITE),
        ("+55 48 99908 2726", 506, 274, 6.30, 82, SOFT_WHITE),
        ("clovis@jus9tecnologia.com.br", 506, 335, 6.30, 82, SOFT_WHITE),
        ("www.jus9tecnologia.com.br", 506, 395, 6.30, 82, SOFT_WHITE),
        ("linkedin.com/company/jus-9-tecnologia-juridica", 506, 456, 6.05, 72, SOFT_WHITE),
    ]
    for text, x, baseline, font_size, horizontal_scale, color in lines:
        text_object = pdf.beginText(
            offset + mm_from_source_x(x),
            offset + mm_from_source_baseline(baseline),
        )
        text_object.setFillColorCMYK(*color)
        text_object.setFont("TimesJus9", font_size)
        text_object.setHorizScale(horizontal_scale)
        text_object.textLine(text)
        pdf.drawText(text_object)


def write_pdf(
    destination: Path,
    pages: list[tuple[Path, Callable[[canvas.Canvas, float], None]]],
    bleed_mm: float,
) -> None:
    width = (TRIM_WIDTH_MM + 2 * bleed_mm) * mm
    height = (TRIM_HEIGHT_MM + 2 * bleed_mm) * mm
    stage = destination.with_suffix(".stage.pdf")
    pdf = canvas.Canvas(
        str(stage),
        pagesize=(width, height),
        pageCompression=1,
        pdfVersion=(1, 4),
    )
    pdf.setTitle("Cartao Jus 9 - Impressao CMYK")
    pdf.setAuthor("Jus 9 Tecnologia Juridica")
    pdf.setCreator("Jus 9 print PDF generator")
    pdf.setSubject("Arte de cartao em CMYK, 600 dpi, com texto vetorial")
    for background, overlay in pages:
        pdf.drawImage(
            str(background),
            0,
            0,
            width=width,
            height=height,
            preserveAspectRatio=False,
        )
        overlay(pdf, bleed_mm * mm)
        pdf.showPage()
    pdf.save()
    add_print_metadata(stage, destination, bleed_mm)
    stage.unlink()


def add_print_metadata(stage: Path, destination: Path, bleed_mm: float) -> None:
    reader = PdfReader(stage)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    writer._header = b"%PDF-1.4"

    icc_stream = DecodedStreamObject()
    icc_stream.set_data(ICC_PROFILE.read_bytes())
    icc_stream.update({NameObject("/N"): NumberObject(4)})
    icc_ref = writer._add_object(icc_stream)

    output_intent = DictionaryObject(
        {
            NameObject("/Type"): NameObject("/OutputIntent"),
            NameObject("/S"): NameObject("/GTS_PDFX"),
            NameObject("/OutputConditionIdentifier"): TextStringObject(
                "U.S. Web Coated (SWOP) v2"
            ),
            NameObject("/Info"): TextStringObject(
                "CMYK output intent: U.S. Web Coated (SWOP) v2"
            ),
            NameObject("/RegistryName"): TextStringObject("http://www.color.org"),
            NameObject("/DestOutputProfile"): icc_ref,
        }
    )
    writer.root_object.update(
        {
            NameObject("/OutputIntents"): ArrayObject(
                [writer._add_object(output_intent)]
            )
        }
    )

    inset = bleed_mm * mm
    for page in writer.pages:
        page[NameObject("/TrimBox")] = RectangleObject(
            [
                FloatObject(inset),
                FloatObject(inset),
                FloatObject(float(page.mediabox.width) - inset),
                FloatObject(float(page.mediabox.height) - inset),
            ]
        )
        page[NameObject("/BleedBox")] = RectangleObject(
            [
                FloatObject(0),
                FloatObject(0),
                FloatObject(float(page.mediabox.width)),
                FloatObject(float(page.mediabox.height)),
            ]
        )

    writer.add_metadata(
        {
            "/Title": "Cartao Jus 9 - Impressao CMYK",
            "/Author": "Jus 9 Tecnologia Juridica",
            "/Creator": "Jus 9 print PDF generator",
            "/Subject": "CMYK, fundo raster 600 dpi, texto pequeno vetorial",
            "/GTS_PDFXVersion": "PDF/X-1a:2001",
            "/GTS_PDFXConformance": "PDF/X-1a:2001",
        }
    )
    with destination.open("wb") as handle:
        writer.write(handle)


def render_preview(pdf_path: Path) -> None:
    with fitz.open(pdf_path) as document:
        for page_number, page in enumerate(document):
            pixmap = page.get_pixmap(dpi=300, alpha=False)
            pixmap.save(
                OUT_DIR / f"{pdf_path.stem}_page-{page_number + 1}_preview.png"
            )


def main() -> None:
    if not ICC_PROFILE.exists():
        raise FileNotFoundError(f"Missing ICC profile: {ICC_PROFILE}")
    if not TIMES_FONT.exists():
        raise FileNotFoundError(f"Missing font: {TIMES_FONT}")
    if not ARIAL_FONT.exists():
        raise FileNotFoundError(f"Missing font: {ARIAL_FONT}")

    OUT_DIR.mkdir(exist_ok=True)
    ASSET_DIR.mkdir(exist_ok=True)
    pdfmetrics.registerFont(TTFont("TimesJus9", str(TIMES_FONT)))
    pdfmetrics.registerFont(TTFont("ArialJus9", str(ARIAL_FONT)))

    downloads = Path.home() / "Downloads"
    original_front = next(downloads.glob("Cart* Frente.pdf"))
    original_back = next(downloads.glob("Cart* Verso.pdf"))

    extracted_front = ASSET_DIR / "front_extracted_cmyk.jpg"
    extracted_back = ASSET_DIR / "back_extracted_cmyk.jpg"
    extract_background(original_front, extracted_front)
    extract_background(original_back, extracted_back)

    backgrounds: dict[tuple[str, float], Path] = {}
    for side, source in (("front", extracted_front), ("back", extracted_back)):
        for bleed in (0.0, BLEED_MM):
            suffix = "trim" if not bleed else "bleed-3mm"
            target = ASSET_DIR / f"{side}_{suffix}_{DPI}dpi_cmyk.jpg"
            improve_background(source, target, bleed, side)
            backgrounds[(side, bleed)] = target

    trim_front = OUT_DIR / "Cartao_Frente_Impressao_CMYK_90x50mm.pdf"
    trim_back = OUT_DIR / "Cartao_Verso_Impressao_CMYK_90x50mm.pdf"
    trim_combined = OUT_DIR / "Cartao_Jus9_Impressao_CMYK_90x50mm.pdf"
    bleed_front = OUT_DIR / "Cartao_Frente_Impressao_CMYK_sangria3mm.pdf"
    bleed_back = OUT_DIR / "Cartao_Verso_Impressao_CMYK_sangria3mm.pdf"
    bleed_combined = OUT_DIR / "Cartao_Jus9_Impressao_CMYK_sangria3mm.pdf"

    write_pdf(trim_front, [(backgrounds[("front", 0.0)], draw_front_overlay)], 0.0)
    write_pdf(trim_back, [(backgrounds[("back", 0.0)], draw_back_overlay)], 0.0)
    write_pdf(
        trim_combined,
        [
            (backgrounds[("front", 0.0)], draw_front_overlay),
            (backgrounds[("back", 0.0)], draw_back_overlay),
        ],
        0.0,
    )
    write_pdf(
        bleed_front,
        [(backgrounds[("front", BLEED_MM)], draw_front_overlay)],
        BLEED_MM,
    )
    write_pdf(
        bleed_back,
        [(backgrounds[("back", BLEED_MM)], draw_back_overlay)],
        BLEED_MM,
    )
    write_pdf(
        bleed_combined,
        [
            (backgrounds[("front", BLEED_MM)], draw_front_overlay),
            (backgrounds[("back", BLEED_MM)], draw_back_overlay),
        ],
        BLEED_MM,
    )

    render_preview(trim_combined)
    render_preview(bleed_combined)

    print(f"Output folder: {OUT_DIR}")
    for pdf_path in sorted(OUT_DIR.glob("*.pdf")):
        print(f"  {pdf_path.name}: {pdf_path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
