"""Generate three fictional purchase-order PDFs and their answer key.

Names, addresses, and amounts live here. One run rewrites the PDFs and
``samples/po/README.md`` together, so the note stays aligned with the pages.

The PDFs are digital text (not scans). Page streams are left uncompressed so
the sample banner and field values stay ordinary selectable text.

Requires reportlab:

    pip install reportlab
    python samples/po/generate_purchase_orders.py
"""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

from reportlab.lib.colors import Color, HexColor, black, white
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

OUT_DIR = Path(__file__).resolve().parent
BANNER = "SAMPLE, fictional purchase order"
MONEY = Decimal("0.01")

BANNER_BG = HexColor("#243044")
MUTED = HexColor("#52606D")
RULE = HexColor("#D5DEE7")
PANEL = HexColor("#F6F8FA")
HEADER_BG = HexColor("#E6EDF4")
ZEBRA = HexColor("#F5F8FB")

MARGIN = 40
CONTENT_WIDTH = letter[0] - 2 * MARGIN
COLUMNS = (
    ("sku", "SKU", 78, "left"),
    ("description", "Description", 220, "left"),
    ("quantity", "Qty", 50, "right"),
    ("unit_price", "Unit price", 92, "right"),
    ("line_total", "Line total", 92, "right"),
)


def money(value: str) -> Decimal:
    """Parse a positive amount that already has two decimal places."""
    amount = Decimal(value)
    if amount.as_tuple().exponent != -2 or amount <= 0:
        raise ValueError(f"{value!r} must be a positive amount with two decimals")
    return amount


def pages_label(pages: list[int]) -> str:
    return ", ".join(str(page) for page in pages)


def table_row(*cells: object) -> str:
    return "| " + " | ".join(str(cell) for cell in cells) + " |"


class Sheet:
    """One page in progress. Origin is the bottom left, in points."""

    def __init__(self, pdf: canvas.Canvas, page: int, page_count: int) -> None:
        self.pdf = pdf
        self.page = page
        self.page_count = page_count
        self.width, self.height = letter
        self.margin = MARGIN
        self.bottom = 56
        self.y = self.height - 48

    def draw_banner(self) -> None:
        self.pdf.setFillColor(BANNER_BG)
        self.pdf.rect(0, self.height - 24, self.width, 24, fill=1, stroke=0)
        draw(self.pdf, self.width / 2, self.height - 16, BANNER, "Helvetica-Bold", 9, white, "center")

    def draw_footer(self, continued: bool) -> None:
        if continued:
            draw(
                self.pdf,
                self.margin,
                34,
                "Lines continue on the next page.",
                "Helvetica",
                8,
                MUTED,
            )
        draw(
            self.pdf,
            self.width - self.margin,
            34,
            f"Page {self.page} of {self.page_count}",
            "Helvetica",
            8,
            MUTED,
            "right",
        )


def draw(
    pdf: canvas.Canvas,
    x: float,
    y: float,
    value: str,
    font: str,
    size: float,
    color: Color,
    align: str = "left",
) -> None:
    if value == "":
        raise ValueError("refusing to draw an empty field")
    pdf.setFillColor(color)
    pdf.setFont(font, size)
    if align == "left":
        pdf.drawString(x, y, value)
    elif align == "right":
        pdf.drawRightString(x, y, value)
    elif align == "center":
        pdf.drawCentredString(x, y, value)
    else:
        raise ValueError(align)


def require_fit(value: str, font: str, size: float, max_width: float) -> None:
    width = stringWidth(value, font, size)
    if width > max_width + 0.2:
        raise ValueError(f"{value!r} is {width:.1f}pt wide and the space is {max_width:.1f}pt")


def party_block(
    pdf: canvas.Canvas,
    x: float,
    top: float,
    width: float,
    party: dict,
) -> float:
    """Draw a labeled name, address, and email. Return the y under the box."""
    pad = 8
    inner = width - 2 * pad
    require_fit(party["label"], "Helvetica-Bold", 8, inner)
    require_fit(party["name"], "Helvetica-Bold", 11, inner)
    require_fit(party["address"], "Helvetica", 9, inner)
    require_fit(party["email"], "Helvetica", 9, inner)

    box_h = 72
    bottom = top - box_h
    pdf.setFillColor(PANEL)
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(0.6)
    pdf.roundRect(x, bottom, width, box_h, 3, fill=1, stroke=1)
    draw(pdf, x + pad, top - 16, party["label"], "Helvetica-Bold", 8, MUTED)
    draw(pdf, x + pad, top - 32, party["name"], "Helvetica-Bold", 11, black)
    draw(pdf, x + pad, top - 46, party["address"], "Helvetica", 9, black)
    draw(pdf, x + pad, top - 60, party["email"], "Helvetica", 9, black)
    return bottom


def party_lines(sheet: Sheet, party: dict) -> None:
    """Plain stacked party, used by the long order so it does not look like the cards."""
    inner = CONTENT_WIDTH
    require_fit(party["name"], "Helvetica-Bold", 11, inner)
    require_fit(party["address"], "Helvetica", 9, inner)
    require_fit(party["email"], "Helvetica", 9, inner)
    draw(sheet.pdf, sheet.margin, sheet.y, party["label"], "Helvetica-Bold", 8, MUTED)
    sheet.y -= 14
    draw(sheet.pdf, sheet.margin, sheet.y, party["name"], "Helvetica-Bold", 11, black)
    sheet.y -= 14
    draw(sheet.pdf, sheet.margin, sheet.y, party["address"], "Helvetica", 9, black)
    sheet.y -= 13
    draw(sheet.pdf, sheet.margin, sheet.y, party["email"], "Helvetica", 9, black)
    sheet.y -= 16


def draw_table(sheet: Sheet, lines: list[dict]) -> None:
    if not lines:
        raise ValueError(f"page {sheet.page} has no lines")
    pdf = sheet.pdf
    x = sheet.margin
    top = sheet.y
    width = sum(column[2] for column in COLUMNS)
    if abs(width - CONTENT_WIDTH) > 0.1:
        raise ValueError("table columns do not fill the page width")
    row_h = 18
    header_h = 18
    height = header_h + row_h * len(lines)
    bottom = top - height
    if bottom < sheet.bottom:
        raise ValueError(f"table overflows page {sheet.page}")

    pdf.setFillColor(HEADER_BG)
    pdf.rect(x, top - header_h, width, header_h, fill=1, stroke=0)
    for index in range(len(lines)):
        if index % 2 == 1:
            row_top = top - header_h - index * row_h
            pdf.setFillColor(ZEBRA)
            pdf.rect(x, row_top - row_h, width, row_h, fill=1, stroke=0)

    def paint(
        value: str,
        left: float,
        col_w: float,
        baseline: float,
        align: str,
        font: str,
        size: float,
        color: Color,
    ) -> None:
        pad = 4
        require_fit(value, font, size, col_w - 2 * pad)
        if align == "left":
            draw(pdf, left + pad, baseline, value, font, size, color)
        else:
            draw(pdf, left + col_w - pad, baseline, value, font, size, color, "right")

    cursor = x
    for _key, label, col_w, align in COLUMNS:
        paint(label, cursor, col_w, top - 12, align, "Helvetica-Bold", 8, MUTED)
        cursor += col_w

    for index, line in enumerate(lines):
        baseline = top - header_h - index * row_h - 12
        values = {
            "sku": line["sku"],
            "description": line["description"],
            "quantity": str(line["quantity"]),
            "unit_price": line["unit_price"],
            "line_total": line["line_total"],
        }
        cursor = x
        for key, _label, col_w, align in COLUMNS:
            paint(values[key], cursor, col_w, baseline, align, "Helvetica", 9, black)
            cursor += col_w

    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(0.4)
    pdf.rect(x, bottom, width, height, fill=0, stroke=1)
    pdf.line(x, top - header_h, x + width, top - header_h)
    cursor = x
    for _key, _label, col_w, _align in COLUMNS[:-1]:
        cursor += col_w
        pdf.line(cursor, bottom, cursor, top)
    for index in range(1, len(lines)):
        rule_y = top - header_h - index * row_h
        pdf.line(x, rule_y, x + width, rule_y)
    sheet.y = bottom - 16


def draw_order_total(sheet: Sheet, order: dict) -> None:
    if sheet.page not in order["order_total"]["pages"]:
        return
    if sheet.y < sheet.bottom + 28:
        raise ValueError(f"order total collides with the footer on page {sheet.page}")
    right = sheet.width - sheet.margin
    amount = order["order_total"]["value"]
    amount_w = stringWidth(amount, "Helvetica-Bold", 12)
    draw(sheet.pdf, right - amount_w - 12, sheet.y, "Order total", "Helvetica", 9, MUTED, "right")
    draw(sheet.pdf, right, sheet.y, amount, "Helvetica-Bold", 12, black, "right")
    if sheet.page in order["currency"]["pages"]:
        currency = order["currency"]["value"]
        currency_w = stringWidth(currency, "Helvetica-Bold", 10)
        draw(sheet.pdf, right - currency_w - 12, sheet.y - 16, "Currency", "Helvetica", 9, MUTED, "right")
        draw(sheet.pdf, right, sheet.y - 16, currency, "Helvetica-Bold", 10, black, "right")
    sheet.y -= 32


def draw_title(sheet: Sheet) -> None:
    draw(sheet.pdf, sheet.margin, sheet.y, "Purchase order", "Helvetica-Bold", 18, black)
    sheet.y -= 28


def draw_meta_stack(sheet: Sheet, order: dict) -> None:
    """PO number, date, and currency, one under another."""
    rows = (
        ("PO number", order["po_number"]),
        ("Order date", order["order_date"]),
        ("Currency", order["currency"]),
    )
    value_x = sheet.margin + 100
    max_width = sheet.width - sheet.margin - value_x
    for label, field in rows:
        if sheet.page not in field["pages"]:
            continue
        require_fit(field["value"], "Helvetica", 11, max_width)
        draw(sheet.pdf, sheet.margin, sheet.y, label, "Helvetica", 9, MUTED)
        draw(sheet.pdf, value_x, sheet.y, field["value"], "Helvetica", 11, black)
        sheet.y -= 18
    sheet.y -= 6


def draw_continuation(sheet: Sheet, po_number: str) -> None:
    draw(sheet.pdf, sheet.margin, sheet.y, "Purchase order", "Helvetica", 10, MUTED)
    x = sheet.margin + stringWidth("Purchase order", "Helvetica", 10) + 8
    draw(sheet.pdf, x, sheet.y, po_number, "Helvetica-Bold", 11, black)
    x += stringWidth(po_number, "Helvetica-Bold", 11) + 8
    draw(sheet.pdf, x, sheet.y, "continued", "Helvetica", 10, MUTED)
    sheet.y -= 22


def new_canvas(path: Path) -> canvas.Canvas:
    pdf = canvas.Canvas(
        str(path),
        pagesize=letter,
        pageCompression=0,
        invariant=1,
        lang="en-US",
    )
    pdf.setTitle("Fictional sample purchase order")
    pdf.setAuthor("Fictional sample")
    pdf.setCreator("samples/po/generate_purchase_orders.py")
    return pdf


def begin_page(pdf: canvas.Canvas, page: int, page_count: int) -> Sheet:
    if page > 1:
        pdf.showPage()
    sheet = Sheet(pdf, page, page_count)
    sheet.draw_banner()
    return sheet


def lines_on(order: dict, page: int) -> list[dict]:
    return [line for line in order["lines"] if line["page"] == page]


def draw_simple_table(path: Path, order: dict) -> None:
    pdf = new_canvas(path)
    sheet = begin_page(pdf, 1, 1)
    draw_title(sheet)
    draw_meta_stack(sheet, order)
    for party in (order["vendor"], order["buyer"]):
        sheet.y = party_block(sheet.pdf, sheet.margin, sheet.y, CONTENT_WIDTH, party) - 12
    draw_table(sheet, lines_on(order, 1))
    draw_order_total(sheet, order)
    sheet.draw_footer(continued=False)
    pdf.save()


def draw_bill_ship_columns(path: Path, order: dict) -> None:
    pdf = new_canvas(path)
    sheet = begin_page(pdf, 1, 1)
    draw_title(sheet)
    gap = 16
    col_w = (CONTENT_WIDTH - gap) / 2
    top = sheet.y
    vendor_bottom = party_block(sheet.pdf, sheet.margin, top, col_w, order["vendor"])
    meta_bottom = meta_card(sheet.pdf, sheet.margin + col_w + gap, top, col_w, order)
    sheet.y = min(vendor_bottom, meta_bottom) - 12
    bill_bottom = party_block(sheet.pdf, sheet.margin, sheet.y, col_w, order["buyer"])
    ship_bottom = party_block(
        sheet.pdf,
        sheet.margin + col_w + gap,
        sheet.y,
        col_w,
        order["ship_to"],
    )
    sheet.y = min(bill_bottom, ship_bottom) - 14
    draw_table(sheet, lines_on(order, 1))
    draw_order_total(sheet, order)
    sheet.draw_footer(continued=False)
    pdf.save()


def meta_card(pdf: canvas.Canvas, x: float, top: float, width: float, order: dict) -> float:
    """Right-hand header card: PO number, date, and currency beside the vendor."""
    box_h = 72
    bottom = top - box_h
    pdf.setFillColor(PANEL)
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(0.6)
    pdf.roundRect(x, bottom, width, box_h, 3, fill=1, stroke=1)
    rows = (
        ("PO number", order["po_number"]["value"]),
        ("Order date", order["order_date"]["value"]),
        ("Currency", order["currency"]["value"]),
    )
    baseline = top - 20
    value_x = x + 78
    max_width = x + width - 8 - value_x
    for label, value in rows:
        require_fit(value, "Helvetica", 10, max_width)
        draw(pdf, x + 8, baseline, label, "Helvetica", 8, MUTED)
        draw(pdf, value_x, baseline, value, "Helvetica", 10, black)
        baseline -= 18
    return bottom


def draw_multipage(path: Path, order: dict) -> None:
    pdf = new_canvas(path)
    page_count = order["pages"]
    for page in range(1, page_count + 1):
        sheet = begin_page(pdf, page, page_count)
        if page == 1:
            draw_title(sheet)
            draw_meta_stack(sheet, order)
            party_lines(sheet, order["vendor"])
            party_lines(sheet, order["buyer"])
            sheet.y -= 4
        else:
            if page not in order["po_number"]["pages"]:
                raise ValueError("continuation page is missing the PO number")
            draw_continuation(sheet, order["po_number"]["value"])
        draw_table(sheet, lines_on(order, page))
        draw_order_total(sheet, order)
        sheet.draw_footer(continued=page < page_count)
    pdf.save()


DRAWERS = {
    "simple-table": draw_simple_table,
    "bill-ship-columns": draw_bill_ship_columns,
    "multipage": draw_multipage,
}


def check_pages(pages: list[int], page_count: int, label: str) -> None:
    if not pages or pages != sorted(pages) or len(pages) != len(set(pages)):
        raise ValueError(f"{label} pages must be a unique ascending list")
    if pages[0] < 1 or pages[-1] > page_count:
        raise ValueError(f"{label} falls outside the document")


def check_party(party: dict, page_count: int, label: str) -> None:
    for key in ("label", "name", "address", "email", "pages"):
        if key not in party:
            raise ValueError(f"{label} is missing {key}")
    if not party["email"].endswith("@example.com"):
        raise ValueError(f"{label} email must use example.com")
    check_pages(party["pages"], page_count, label)


def validate(order: dict) -> None:
    """Refuse a fixture whose key would disagree with what the pages draw."""
    page_count = order["pages"]
    layout = order["layout"]
    if layout not in DRAWERS:
        raise ValueError(layout)
    if layout == "simple-table" and (page_count != 1 or "ship_to" in order):
        raise ValueError("the simple table is one page and has no ship-to block")
    if layout == "bill-ship-columns" and (page_count != 1 or "ship_to" not in order):
        raise ValueError("the column layout needs one page and a ship-to block")
    if layout == "multipage":
        if page_count not in (2, 3):
            raise ValueError("the long order is 2 or 3 pages")
        if order["order_total"]["pages"] != [page_count]:
            raise ValueError("the order total belongs on the last page only")
        if order["po_number"]["pages"] != list(range(1, page_count + 1)):
            raise ValueError("the PO number is repeated on every page")

    if layout in ("simple-table", "bill-ship-columns"):
        for label in ("po_number", "order_date", "currency", "order_total"):
            if order[label]["pages"] != [1]:
                raise ValueError(f"{label} should be on page 1")
        for label in ("vendor", "buyer"):
            if order[label]["pages"] != [1]:
                raise ValueError(f"{label} should be on page 1")

    check_pages(order["po_number"]["pages"], page_count, "PO number")
    check_pages(order["order_date"]["pages"], page_count, "order date")
    check_pages(order["currency"]["pages"], page_count, "currency")
    check_pages(order["order_total"]["pages"], page_count, "order total")
    if order["currency"]["value"] not in {"USD", "EUR", "GBP"}:
        raise ValueError("currency must be USD, EUR, or GBP")
    for page in order["order_total"]["pages"]:
        if page not in order["currency"]["pages"]:
            raise ValueError("currency is printed beside the order total")

    check_party(order["vendor"], page_count, "vendor")
    check_party(order["buyer"], page_count, "buyer")
    if "ship_to" in order:
        check_party(order["ship_to"], page_count, "ship-to")
        if order["ship_to"]["label"] != "SHIP TO":
            raise ValueError("ship-to label must read SHIP TO")

    line_pages = [line["page"] for line in order["lines"]]
    if not line_pages or line_pages != sorted(line_pages):
        raise ValueError("lines should be grouped by page")
    if set(line_pages) != set(range(1, page_count + 1)):
        raise ValueError("every page should carry at least one line")
    skus = [line["sku"] for line in order["lines"]]
    if len(skus) != len(set(skus)):
        raise ValueError("duplicate SKU")

    total = Decimal("0.00")
    for line in order["lines"]:
        price = money(line["unit_price"])
        quantity = line["quantity"]
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError(f"{line['sku']} quantity")
        expect = (price * quantity).quantize(MONEY)
        if Decimal(line["line_total"]) != expect:
            raise ValueError(f"{line['sku']} line total")
        if not 1 <= line["page"] <= page_count:
            raise ValueError(f"{line['sku']} page")
        total += expect
    if Decimal(order["order_total"]["value"]) != total:
        raise ValueError(
            f"{order['file']} total is {order['order_total']['value']}, lines sum to {total:.2f}"
        )


def make_line(sku: str, description: str, quantity: int, unit_price: str, page: int) -> dict:
    price = money(unit_price)
    line_total = (price * quantity).quantize(MONEY)
    return {
        "sku": sku,
        "description": description,
        "quantity": quantity,
        "unit_price": f"{price:.2f}",
        "line_total": f"{line_total:.2f}",
        "page": page,
    }


def party(label: str, name: str, address: str, email: str, pages: list[int]) -> dict:
    return {
        "label": label,
        "name": name,
        "address": address,
        "email": email,
        "pages": pages,
    }


def build_orders() -> list[dict]:
    simple_lines = [
        make_line("HP-2201", "Uncoated copy paper, ream", 10, "6.40", 1),
        make_line("HP-1180", "Ballpoint pens, box of 12", 6, "4.25", 1),
        make_line("HP-3304", "Manila folders, pack of 25", 8, "7.15", 1),
        make_line("HP-0902", "Binder clips, assorted", 3, "5.90", 1),
    ]
    column_lines = [
        make_line("BK-014", "Stoneware mug, slate glaze", 24, "8.50", 1),
        make_line("BK-027", "Dinner plate, 10 inch", 24, "11.00", 1),
        make_line("BK-033", "Large serving bowl", 12, "16.75", 1),
        make_line("BK-041", "Sand linen napkin", 40, "3.20", 1),
        make_line("BK-052", "Teaspoon, brushed steel", 36, "2.45", 1),
    ]
    long_lines = [
        make_line("NR-1001", "Digital caliper, 150 mm", 5, "24.00", 1),
        make_line("NR-1002", "Steel ruler, 300 mm", 12, "3.50", 1),
        make_line("NR-1003", "Grid notebook, A4", 20, "4.80", 1),
        make_line("NR-1004", "Safety goggles", 15, "6.25", 1),
        make_line("NR-1005", "Nitrile gloves, box of 100", 10, "8.90", 1),
        make_line("NR-1006", "Isopropyl wipes, pack of 50", 18, "2.40", 1),
        make_line("NR-1007", "Cable ties, pack of 200", 7, "5.15", 1),
        make_line("NR-1008", "White label tape", 9, "11.30", 1),
        make_line("NR-1009", "LED bench lamp", 4, "32.50", 1),
        make_line("NR-1010", "Storage bin, 12 liter", 16, "4.75", 1),
        make_line("NR-1011", "Letter clipboard", 14, "2.85", 1),
        make_line("NR-1012", "Packing tape, 6 rolls", 8, "9.60", 1),
        make_line("NR-1013", "Black permanent marker", 30, "1.25", 2),
        make_line("NR-1014", "First aid refill kit", 3, "18.40", 2),
        make_line("NR-1015", "Extension cord, 5 meter", 6, "13.75", 2),
        make_line("NR-1016", "Large desk mat", 5, "21.00", 2),
        make_line("NR-1017", "Two-step stool", 2, "45.00", 2),
        make_line("NR-1018", "Silent wall clock", 6, "14.50", 2),
        make_line("NR-1019", "Waste bin, 20 liter", 8, "9.95", 2),
        make_line("NR-1020", "Hand soap, carton of 4", 4, "12.80", 2),
        make_line("NR-1021", "Paper towel, carton", 6, "15.20", 2),
        make_line("NR-1022", "Broom with dustpan", 4, "11.45", 2),
        make_line("NR-1023", "Doorstop wedge", 12, "2.15", 2),
        make_line("NR-1024", "Shelf label holder", 20, "1.85", 2),
        make_line("NR-1025", "Key cabinet, 20 hooks", 1, "36.00", 3),
        make_line("NR-1026", "Wet floor sign", 5, "8.70", 3),
        make_line("NR-1027", "Batteries, AA pack of 20", 9, "7.60", 3),
        make_line("NR-1028", "Utility knife", 6, "4.35", 3),
        make_line("NR-1029", "Clear storage box", 10, "3.90", 3),
        make_line("NR-1030", "Wall hook, pack of 6", 8, "5.55", 3),
    ]

    orders = [
        {
            "file": "01-simple-table.pdf",
            "layout": "simple-table",
            "summary": "One-page table. Vendor and buyer are stacked above the lines. The total is on that page.",
            "pages": 1,
            "po_number": {"value": "PO-1847", "pages": [1]},
            "order_date": {"value": "February 3, 2026", "pages": [1]},
            "vendor": party(
                "VENDOR",
                "Harbor and Pine Supply",
                "18 Cedar Lane, Mapleford, Exampleland",
                "sales@example.com",
                [1],
            ),
            "buyer": party(
                "BUYER",
                "Linden Reading Room",
                "4 North Dock Street, Cedarholm, Exampleland",
                "buying@example.com",
                [1],
            ),
            "currency": {"value": "USD", "pages": [1]},
            "lines": simple_lines,
            "order_total": {"value": _sum(simple_lines), "pages": [1]},
        },
        {
            "file": "02-bill-ship-columns.pdf",
            "layout": "bill-ship-columns",
            "summary": "Two-column header. Bill to and ship to sit side by side. The total is on that page.",
            "pages": 1,
            "po_number": {"value": "PO-2026-077", "pages": [1]},
            "order_date": {"value": "April 18, 2026", "pages": [1]},
            "vendor": party(
                "VENDOR",
                "Brightkiln Studio",
                "420 Kiln Road, Redclay, Exampleland",
                "studio@example.com",
                [1],
            ),
            "buyer": party(
                "BILL TO",
                "Paperwhistle Atelier",
                "88 Willow Court, West Larkspur, Exampleland",
                "accounts@example.com",
                [1],
            ),
            "ship_to": party(
                "SHIP TO",
                "Paperwhistle Atelier Warehouse",
                "15 Loading Dock Way, West Larkspur, Exampleland",
                "receiving@example.com",
                [1],
            ),
            "currency": {"value": "EUR", "pages": [1]},
            "lines": column_lines,
            "order_total": {"value": _sum(column_lines), "pages": [1]},
        },
        {
            "file": "03-multipage-lines.pdf",
            "layout": "multipage",
            "summary": "Three pages. Lines continue past page 1. The total is on the last page only.",
            "pages": 3,
            "po_number": {"value": "PO-55910", "pages": [1, 2, 3]},
            "order_date": {"value": "January 22, 2026", "pages": [1]},
            "vendor": party(
                "VENDOR",
                "North Wren Instruments",
                "90 Station Yard, Brindleford, Exampleland",
                "orders@example.com",
                [1],
            ),
            "buyer": party(
                "BILL TO",
                "Larkspur Schools Facilities",
                "2 Orchard Road, North Wren, Exampleland",
                "facilities@example.com",
                [1],
            ),
            "currency": {"value": "GBP", "pages": [1, 3]},
            "lines": long_lines,
            "order_total": {"value": _sum(long_lines), "pages": [3]},
        },
    ]
    for order in orders:
        validate(order)
    return orders


def _sum(lines: list[dict]) -> str:
    total = sum((Decimal(line["line_total"]) for line in lines), Decimal("0.00"))
    return f"{total:.2f}"


def party_rows(prefix: str, party_fields: dict) -> list[str]:
    pages = pages_label(party_fields["pages"])
    return [
        table_row(f"{prefix} label", party_fields["label"], pages),
        table_row(f"{prefix} name", party_fields["name"], pages),
        table_row(f"{prefix} address", party_fields["address"], pages),
        table_row(f"{prefix} email", party_fields["email"], pages),
    ]


def render_readme(orders: list[dict]) -> str:
    lines: list[str] = [
        "# Sample purchase orders",
        "",
        "Three fictional purchase-order PDFs for later extraction scoring.",
        'Every page is marked "SAMPLE, fictional purchase order".',
        "Vendors, buyers, addresses, and amounts are made up.",
        "Mail uses example.com. There are no phone numbers.",
        "These files are not receipt samples, and they are not on the ingest allowlist.",
        "",
        "This note is the answer key.",
        "Each value is listed with the page it is printed on.",
        "A line total is quantity times unit price. The order total is the sum of the line totals.",
        "The banner, the page count, and the line that says lines continue are page chrome, not order fields.",
        "",
        "Regenerate the PDFs and this note from the repo root:",
        "",
        "```bash",
        "pip install reportlab",
        "python samples/po/generate_purchase_orders.py",
        "```",
        "",
        "The JSON block at the end is the same key. `tests/test_po_samples.py` reads it.",
        "",
        "## Files",
        "",
        "| File | Layout | Pages |",
        "| --- | --- | --- |",
    ]
    for order in orders:
        lines.append(table_row(f"[{order['file']}]({order['file']})", order["summary"], order["pages"]))

    for order in orders:
        lines.extend(
            [
                "",
                f"## {order['file']}",
                "",
                order["summary"],
                "",
                "### Fields",
                "",
                "| Field | Value | Pages |",
                "| --- | --- | --- |",
                table_row("PO number", order["po_number"]["value"], pages_label(order["po_number"]["pages"])),
                table_row("Order date", order["order_date"]["value"], pages_label(order["order_date"]["pages"])),
            ]
        )
        lines.extend(party_rows("Vendor", order["vendor"]))
        lines.extend(party_rows("Buyer", order["buyer"]))
        if "ship_to" in order:
            lines.extend(party_rows("Ship-to", order["ship_to"]))
        lines.append(
            table_row("Currency", order["currency"]["value"], pages_label(order["currency"]["pages"]))
        )
        lines.append(
            table_row(
                "Order total",
                order["order_total"]["value"],
                pages_label(order["order_total"]["pages"]),
            )
        )
        lines.extend(
            [
                "",
                "### Lines",
                "",
                "| Page | SKU | Description | Quantity | Unit price | Line total |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for line in order["lines"]:
            lines.append(
                table_row(
                    line["page"],
                    line["sku"],
                    line["description"],
                    line["quantity"],
                    line["unit_price"],
                    line["line_total"],
                )
            )

    payload = {"banner": BANNER, "orders": orders}
    lines.extend(
        [
            "",
            "## Answer key",
            "",
            "Machine-readable copy of the tables above. The test reads this block.",
            "",
            "```json",
            json.dumps(payload, indent=2),
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    orders = build_orders()
    for order in orders:
        destination = OUT_DIR / order["file"]
        DRAWERS[order["layout"]](destination, order)
        print(
            f"{order['file']}: {order['pages']} page(s), "
            f"total {order['order_total']['value']} {order['currency']['value']}"
        )
    readme = OUT_DIR / "README.md"
    readme.write_text(render_readme(orders), encoding="utf-8")
    print(f"wrote {readme.name}")


if __name__ == "__main__":
    main()
