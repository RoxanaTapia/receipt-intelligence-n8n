"""Check the purchase-order answer key and the PDFs it describes.

``samples/po/README.md`` is the scoring key. The test reads that note, not
the generator, so it does not need reportlab. It checks the arithmetic, that
each listed PDF exists, and that the page count matches the note.
"""

from __future__ import annotations

import json
import re
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PO_DIR = ROOT / "samples" / "po"
README = PO_DIR / "README.md"
MONEY = Decimal("0.01")
PAGE_RE = re.compile(rb"/Type\s*/Page(?!s)")
EMAIL_RE = re.compile(r"[\w.+-]+@([\w.-]+)")

EXPECTED_FILES = (
    "01-simple-table.pdf",
    "02-bill-ship-columns.pdf",
    "03-multipage-lines.pdf",
)


def load_answer_key(readme: Path = README) -> dict:
    """Pull the JSON block under the Answer key heading."""
    text = readme.read_text(encoding="utf-8")
    heading = text.index("## Answer key")
    fence = text.index("```json", heading)
    body_start = text.index("\n", fence) + 1
    body_end = text.index("```", body_start)
    return json.loads(text[body_start:body_end])


def pdf_page_count(path: Path) -> int:
    """Count page objects in an uncompressed reportlab PDF.

    ``/Type /Pages`` is the tree node, so it does not count as a page.
    """
    data = path.read_bytes()
    if not data.startswith(b"%PDF"):
        raise AssertionError(f"{path.name} is not a PDF")
    return len(PAGE_RE.findall(data))


def pages_label(pages: list[int]) -> str:
    return ", ".join(str(page) for page in pages)


def table_row(*cells: object) -> str:
    return "| " + " | ".join(str(cell) for cell in cells) + " |"


class PurchaseOrderSamplesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.key = load_answer_key()
        cls.readme = README.read_text(encoding="utf-8")

    def test_catalog_matches_the_folder(self) -> None:
        files = [order["file"] for order in self.key["orders"]]
        self.assertEqual(list(EXPECTED_FILES), files)
        self.assertEqual({path.name for path in PO_DIR.glob("*.pdf")}, set(EXPECTED_FILES))
        self.assertEqual(self.key["banner"], "SAMPLE, fictional purchase order")

    def test_answer_key_arithmetic_and_pdf_pages(self) -> None:
        for order in self.key["orders"]:
            with self.subTest(order=order["file"]):
                self.check_order(order)

    def test_layouts(self) -> None:
        orders = {order["file"]: order for order in self.key["orders"]}

        simple = orders["01-simple-table.pdf"]
        self.assertEqual(simple["layout"], "simple-table")
        self.assertEqual(simple["pages"], 1)
        self.assertNotIn("ship_to", simple)
        self.assertEqual(simple["buyer"]["label"], "BUYER")
        self.assertEqual(simple["order_total"]["pages"], [1])

        columns = orders["02-bill-ship-columns.pdf"]
        self.assertEqual(columns["layout"], "bill-ship-columns")
        self.assertEqual(columns["pages"], 1)
        self.assertEqual(columns["buyer"]["label"], "BILL TO")
        self.assertEqual(columns["ship_to"]["label"], "SHIP TO")
        self.assertEqual(columns["order_total"]["pages"], [1])

        multi = orders["03-multipage-lines.pdf"]
        self.assertEqual(multi["layout"], "multipage")
        self.assertIn(multi["pages"], (2, 3))
        self.assertEqual(multi["order_total"]["pages"], [multi["pages"]])
        self.assertEqual(multi["po_number"]["pages"], list(range(1, multi["pages"] + 1)))
        self.assertIn(1, multi["currency"]["pages"])
        self.assertIn(multi["pages"], multi["currency"]["pages"])
        line_pages = {line["page"] for line in multi["lines"]}
        self.assertIn(1, line_pages)
        self.assertIn(multi["pages"], line_pages)
        self.assertTrue(any(page < multi["pages"] for page in line_pages))

    def test_emails_use_example_com(self) -> None:
        blob = json.dumps(self.key)
        domains = {match.group(1) for match in EMAIL_RE.finditer(blob)}
        self.assertEqual(domains, {"example.com"})

    def check_order(self, order: dict) -> None:
        page_count = order["pages"]
        self.assertIsInstance(page_count, int)
        self.assertGreaterEqual(page_count, 1)

        total = Decimal("0.00")
        seen_pages: set[int] = set()
        for line in order["lines"]:
            quantity = line["quantity"]
            self.assertIsInstance(quantity, int)
            self.assertGreater(quantity, 0)
            unit = Decimal(line["unit_price"])
            line_total = Decimal(line["line_total"])
            self.assertEqual((unit * quantity).quantize(MONEY), line_total)
            self.assertIn(line["page"], range(1, page_count + 1))
            seen_pages.add(line["page"])
            total += line_total
            row = table_row(
                line["page"],
                line["sku"],
                line["description"],
                quantity,
                line["unit_price"],
                line["line_total"],
            )
            self.assertIn(row, self.readme)

        self.assertEqual(seen_pages, set(range(1, page_count + 1)))
        self.assertEqual(Decimal(order["order_total"]["value"]), total)
        self.assert_field_row("PO number", order["po_number"], page_count)
        self.assert_field_row("Order date", order["order_date"], page_count)
        self.assert_field_row("Currency", order["currency"], page_count)
        self.assert_field_row("Order total", order["order_total"], page_count)
        self.assert_party_rows("Vendor", order["vendor"], page_count)
        self.assert_party_rows("Buyer", order["buyer"], page_count)
        if "ship_to" in order:
            self.assert_party_rows("Ship-to", order["ship_to"], page_count)

        path = PO_DIR / order["file"]
        self.assertTrue(path.is_file(), f"missing {path}")
        self.assertEqual(pdf_page_count(path), page_count)

        # Page streams are uncompressed, so field values are literal PDF strings.
        raw = path.read_bytes().decode("latin-1")
        self.assertEqual(raw.count(f"({self.key['banner']})"), page_count)
        self.assertGreaterEqual(
            raw.count(f"({order['po_number']['value']})"),
            len(order["po_number"]["pages"]),
        )
        self.assertIn(f"({order['order_date']['value']})", raw)
        self.assertIn(f"({order['currency']['value']})", raw)
        self.assertIn(f"({order['order_total']['value']})", raw)
        self.assertEqual(raw.count("(Order total)"), 1)
        continued = "(Lines continue on the next page.)"
        if page_count == 1:
            self.assertNotIn(continued, raw)
        else:
            self.assertEqual(raw.count(continued), page_count - 1)

        for party in ("vendor", "buyer"):
            self.assert_party_in_pdf(raw, order[party])
        if "ship_to" in order:
            self.assert_party_in_pdf(raw, order["ship_to"])

    def assert_field_row(self, label: str, field: dict, page_count: int) -> None:
        self.assertIn(table_row(label, field["value"], pages_label(field["pages"])), self.readme)
        for page in field["pages"]:
            self.assertIn(page, range(1, page_count + 1))

    def assert_party_rows(self, prefix: str, party: dict, page_count: int) -> None:
        for page in party["pages"]:
            self.assertIn(page, range(1, page_count + 1))
        pages = pages_label(party["pages"])
        for label, value in (
            (f"{prefix} label", party["label"]),
            (f"{prefix} name", party["name"]),
            (f"{prefix} address", party["address"]),
            (f"{prefix} email", party["email"]),
        ):
            self.assertIn(table_row(label, value, pages), self.readme)
        self.assertTrue(party["email"].endswith("@example.com"))

    def assert_party_in_pdf(self, raw: str, party: dict) -> None:
        for field in ("label", "name", "address", "email"):
            self.assertIn(f"({party[field]})", raw)


if __name__ == "__main__":
    unittest.main()
