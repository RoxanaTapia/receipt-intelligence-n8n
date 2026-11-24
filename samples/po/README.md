# Sample purchase orders

Three fictional purchase-order PDFs for later extraction scoring.
Every page is marked "SAMPLE, fictional purchase order".
Vendors, buyers, addresses, and amounts are made up.
Mail uses example.com. There are no phone numbers.
These files are not receipt samples, and they are not on the ingest allowlist.

This note is the answer key.
Each value is listed with the page it is printed on.
A line total is quantity times unit price. The order total is the sum of the line totals.
The banner, the page count, and the line that says lines continue are page chrome, not order fields.

Regenerate the PDFs and this note from the repo root:

```bash
pip install reportlab
python samples/po/generate_purchase_orders.py
```

The JSON block at the end is the same key. `tests/test_po_samples.py` reads it.

## Files

| File | Layout | Pages |
| --- | --- | --- |
| [01-simple-table.pdf](01-simple-table.pdf) | One-page table. Vendor and buyer are stacked above the lines. The total is on that page. | 1 |
| [02-bill-ship-columns.pdf](02-bill-ship-columns.pdf) | Two-column header. Bill to and ship to sit side by side. The total is on that page. | 1 |
| [03-multipage-lines.pdf](03-multipage-lines.pdf) | Three pages. Lines continue past page 1. The total is on the last page only. | 3 |

## 01-simple-table.pdf

One-page table. Vendor and buyer are stacked above the lines. The total is on that page.

### Fields

| Field | Value | Pages |
| --- | --- | --- |
| PO number | PO-1847 | 1 |
| Order date | February 3, 2026 | 1 |
| Vendor label | VENDOR | 1 |
| Vendor name | Harbor and Pine Supply | 1 |
| Vendor address | 18 Cedar Lane, Mapleford, Exampleland | 1 |
| Vendor email | sales@example.com | 1 |
| Buyer label | BUYER | 1 |
| Buyer name | Linden Reading Room | 1 |
| Buyer address | 4 North Dock Street, Cedarholm, Exampleland | 1 |
| Buyer email | buying@example.com | 1 |
| Currency | USD | 1 |
| Order total | 164.40 | 1 |

### Lines

| Page | SKU | Description | Quantity | Unit price | Line total |
| --- | --- | --- | --- | --- | --- |
| 1 | HP-2201 | Uncoated copy paper, ream | 10 | 6.40 | 64.00 |
| 1 | HP-1180 | Ballpoint pens, box of 12 | 6 | 4.25 | 25.50 |
| 1 | HP-3304 | Manila folders, pack of 25 | 8 | 7.15 | 57.20 |
| 1 | HP-0902 | Binder clips, assorted | 3 | 5.90 | 17.70 |

## 02-bill-ship-columns.pdf

Two-column header. Bill to and ship to sit side by side. The total is on that page.

### Fields

| Field | Value | Pages |
| --- | --- | --- |
| PO number | PO-2026-077 | 1 |
| Order date | April 18, 2026 | 1 |
| Vendor label | VENDOR | 1 |
| Vendor name | Brightkiln Studio | 1 |
| Vendor address | 420 Kiln Road, Redclay, Exampleland | 1 |
| Vendor email | studio@example.com | 1 |
| Buyer label | BILL TO | 1 |
| Buyer name | Paperwhistle Atelier | 1 |
| Buyer address | 88 Willow Court, West Larkspur, Exampleland | 1 |
| Buyer email | accounts@example.com | 1 |
| Ship-to label | SHIP TO | 1 |
| Ship-to name | Paperwhistle Atelier Warehouse | 1 |
| Ship-to address | 15 Loading Dock Way, West Larkspur, Exampleland | 1 |
| Ship-to email | receiving@example.com | 1 |
| Currency | EUR | 1 |
| Order total | 885.20 | 1 |

### Lines

| Page | SKU | Description | Quantity | Unit price | Line total |
| --- | --- | --- | --- | --- | --- |
| 1 | BK-014 | Stoneware mug, slate glaze | 24 | 8.50 | 204.00 |
| 1 | BK-027 | Dinner plate, 10 inch | 24 | 11.00 | 264.00 |
| 1 | BK-033 | Large serving bowl | 12 | 16.75 | 201.00 |
| 1 | BK-041 | Sand linen napkin | 40 | 3.20 | 128.00 |
| 1 | BK-052 | Teaspoon, brushed steel | 36 | 2.45 | 88.20 |

## 03-multipage-lines.pdf

Three pages. Lines continue past page 1. The total is on the last page only.

### Fields

| Field | Value | Pages |
| --- | --- | --- |
| PO number | PO-55910 | 1, 2, 3 |
| Order date | January 22, 2026 | 1 |
| Vendor label | VENDOR | 1 |
| Vendor name | North Wren Instruments | 1 |
| Vendor address | 90 Station Yard, Brindleford, Exampleland | 1 |
| Vendor email | orders@example.com | 1 |
| Buyer label | BILL TO | 1 |
| Buyer name | Larkspur Schools Facilities | 1 |
| Buyer address | 2 Orchard Road, North Wren, Exampleland | 1 |
| Buyer email | facilities@example.com | 1 |
| Currency | GBP | 1, 3 |
| Order total | 1989.60 | 3 |

### Lines

| Page | SKU | Description | Quantity | Unit price | Line total |
| --- | --- | --- | --- | --- | --- |
| 1 | NR-1001 | Digital caliper, 150 mm | 5 | 24.00 | 120.00 |
| 1 | NR-1002 | Steel ruler, 300 mm | 12 | 3.50 | 42.00 |
| 1 | NR-1003 | Grid notebook, A4 | 20 | 4.80 | 96.00 |
| 1 | NR-1004 | Safety goggles | 15 | 6.25 | 93.75 |
| 1 | NR-1005 | Nitrile gloves, box of 100 | 10 | 8.90 | 89.00 |
| 1 | NR-1006 | Isopropyl wipes, pack of 50 | 18 | 2.40 | 43.20 |
| 1 | NR-1007 | Cable ties, pack of 200 | 7 | 5.15 | 36.05 |
| 1 | NR-1008 | White label tape | 9 | 11.30 | 101.70 |
| 1 | NR-1009 | LED bench lamp | 4 | 32.50 | 130.00 |
| 1 | NR-1010 | Storage bin, 12 liter | 16 | 4.75 | 76.00 |
| 1 | NR-1011 | Letter clipboard | 14 | 2.85 | 39.90 |
| 1 | NR-1012 | Packing tape, 6 rolls | 8 | 9.60 | 76.80 |
| 2 | NR-1013 | Black permanent marker | 30 | 1.25 | 37.50 |
| 2 | NR-1014 | First aid refill kit | 3 | 18.40 | 55.20 |
| 2 | NR-1015 | Extension cord, 5 meter | 6 | 13.75 | 82.50 |
| 2 | NR-1016 | Large desk mat | 5 | 21.00 | 105.00 |
| 2 | NR-1017 | Two-step stool | 2 | 45.00 | 90.00 |
| 2 | NR-1018 | Silent wall clock | 6 | 14.50 | 87.00 |
| 2 | NR-1019 | Waste bin, 20 liter | 8 | 9.95 | 79.60 |
| 2 | NR-1020 | Hand soap, carton of 4 | 4 | 12.80 | 51.20 |
| 2 | NR-1021 | Paper towel, carton | 6 | 15.20 | 91.20 |
| 2 | NR-1022 | Broom with dustpan | 4 | 11.45 | 45.80 |
| 2 | NR-1023 | Doorstop wedge | 12 | 2.15 | 25.80 |
| 2 | NR-1024 | Shelf label holder | 20 | 1.85 | 37.00 |
| 3 | NR-1025 | Key cabinet, 20 hooks | 1 | 36.00 | 36.00 |
| 3 | NR-1026 | Wet floor sign | 5 | 8.70 | 43.50 |
| 3 | NR-1027 | Batteries, AA pack of 20 | 9 | 7.60 | 68.40 |
| 3 | NR-1028 | Utility knife | 6 | 4.35 | 26.10 |
| 3 | NR-1029 | Clear storage box | 10 | 3.90 | 39.00 |
| 3 | NR-1030 | Wall hook, pack of 6 | 8 | 5.55 | 44.40 |

## Answer key

Machine-readable copy of the tables above. The test reads this block.

```json
{
  "banner": "SAMPLE, fictional purchase order",
  "orders": [
    {
      "file": "01-simple-table.pdf",
      "layout": "simple-table",
      "summary": "One-page table. Vendor and buyer are stacked above the lines. The total is on that page.",
      "pages": 1,
      "po_number": {
        "value": "PO-1847",
        "pages": [
          1
        ]
      },
      "order_date": {
        "value": "February 3, 2026",
        "pages": [
          1
        ]
      },
      "vendor": {
        "label": "VENDOR",
        "name": "Harbor and Pine Supply",
        "address": "18 Cedar Lane, Mapleford, Exampleland",
        "email": "sales@example.com",
        "pages": [
          1
        ]
      },
      "buyer": {
        "label": "BUYER",
        "name": "Linden Reading Room",
        "address": "4 North Dock Street, Cedarholm, Exampleland",
        "email": "buying@example.com",
        "pages": [
          1
        ]
      },
      "currency": {
        "value": "USD",
        "pages": [
          1
        ]
      },
      "lines": [
        {
          "sku": "HP-2201",
          "description": "Uncoated copy paper, ream",
          "quantity": 10,
          "unit_price": "6.40",
          "line_total": "64.00",
          "page": 1
        },
        {
          "sku": "HP-1180",
          "description": "Ballpoint pens, box of 12",
          "quantity": 6,
          "unit_price": "4.25",
          "line_total": "25.50",
          "page": 1
        },
        {
          "sku": "HP-3304",
          "description": "Manila folders, pack of 25",
          "quantity": 8,
          "unit_price": "7.15",
          "line_total": "57.20",
          "page": 1
        },
        {
          "sku": "HP-0902",
          "description": "Binder clips, assorted",
          "quantity": 3,
          "unit_price": "5.90",
          "line_total": "17.70",
          "page": 1
        }
      ],
      "order_total": {
        "value": "164.40",
        "pages": [
          1
        ]
      }
    },
    {
      "file": "02-bill-ship-columns.pdf",
      "layout": "bill-ship-columns",
      "summary": "Two-column header. Bill to and ship to sit side by side. The total is on that page.",
      "pages": 1,
      "po_number": {
        "value": "PO-2026-077",
        "pages": [
          1
        ]
      },
      "order_date": {
        "value": "April 18, 2026",
        "pages": [
          1
        ]
      },
      "vendor": {
        "label": "VENDOR",
        "name": "Brightkiln Studio",
        "address": "420 Kiln Road, Redclay, Exampleland",
        "email": "studio@example.com",
        "pages": [
          1
        ]
      },
      "buyer": {
        "label": "BILL TO",
        "name": "Paperwhistle Atelier",
        "address": "88 Willow Court, West Larkspur, Exampleland",
        "email": "accounts@example.com",
        "pages": [
          1
        ]
      },
      "ship_to": {
        "label": "SHIP TO",
        "name": "Paperwhistle Atelier Warehouse",
        "address": "15 Loading Dock Way, West Larkspur, Exampleland",
        "email": "receiving@example.com",
        "pages": [
          1
        ]
      },
      "currency": {
        "value": "EUR",
        "pages": [
          1
        ]
      },
      "lines": [
        {
          "sku": "BK-014",
          "description": "Stoneware mug, slate glaze",
          "quantity": 24,
          "unit_price": "8.50",
          "line_total": "204.00",
          "page": 1
        },
        {
          "sku": "BK-027",
          "description": "Dinner plate, 10 inch",
          "quantity": 24,
          "unit_price": "11.00",
          "line_total": "264.00",
          "page": 1
        },
        {
          "sku": "BK-033",
          "description": "Large serving bowl",
          "quantity": 12,
          "unit_price": "16.75",
          "line_total": "201.00",
          "page": 1
        },
        {
          "sku": "BK-041",
          "description": "Sand linen napkin",
          "quantity": 40,
          "unit_price": "3.20",
          "line_total": "128.00",
          "page": 1
        },
        {
          "sku": "BK-052",
          "description": "Teaspoon, brushed steel",
          "quantity": 36,
          "unit_price": "2.45",
          "line_total": "88.20",
          "page": 1
        }
      ],
      "order_total": {
        "value": "885.20",
        "pages": [
          1
        ]
      }
    },
    {
      "file": "03-multipage-lines.pdf",
      "layout": "multipage",
      "summary": "Three pages. Lines continue past page 1. The total is on the last page only.",
      "pages": 3,
      "po_number": {
        "value": "PO-55910",
        "pages": [
          1,
          2,
          3
        ]
      },
      "order_date": {
        "value": "January 22, 2026",
        "pages": [
          1
        ]
      },
      "vendor": {
        "label": "VENDOR",
        "name": "North Wren Instruments",
        "address": "90 Station Yard, Brindleford, Exampleland",
        "email": "orders@example.com",
        "pages": [
          1
        ]
      },
      "buyer": {
        "label": "BILL TO",
        "name": "Larkspur Schools Facilities",
        "address": "2 Orchard Road, North Wren, Exampleland",
        "email": "facilities@example.com",
        "pages": [
          1
        ]
      },
      "currency": {
        "value": "GBP",
        "pages": [
          1,
          3
        ]
      },
      "lines": [
        {
          "sku": "NR-1001",
          "description": "Digital caliper, 150 mm",
          "quantity": 5,
          "unit_price": "24.00",
          "line_total": "120.00",
          "page": 1
        },
        {
          "sku": "NR-1002",
          "description": "Steel ruler, 300 mm",
          "quantity": 12,
          "unit_price": "3.50",
          "line_total": "42.00",
          "page": 1
        },
        {
          "sku": "NR-1003",
          "description": "Grid notebook, A4",
          "quantity": 20,
          "unit_price": "4.80",
          "line_total": "96.00",
          "page": 1
        },
        {
          "sku": "NR-1004",
          "description": "Safety goggles",
          "quantity": 15,
          "unit_price": "6.25",
          "line_total": "93.75",
          "page": 1
        },
        {
          "sku": "NR-1005",
          "description": "Nitrile gloves, box of 100",
          "quantity": 10,
          "unit_price": "8.90",
          "line_total": "89.00",
          "page": 1
        },
        {
          "sku": "NR-1006",
          "description": "Isopropyl wipes, pack of 50",
          "quantity": 18,
          "unit_price": "2.40",
          "line_total": "43.20",
          "page": 1
        },
        {
          "sku": "NR-1007",
          "description": "Cable ties, pack of 200",
          "quantity": 7,
          "unit_price": "5.15",
          "line_total": "36.05",
          "page": 1
        },
        {
          "sku": "NR-1008",
          "description": "White label tape",
          "quantity": 9,
          "unit_price": "11.30",
          "line_total": "101.70",
          "page": 1
        },
        {
          "sku": "NR-1009",
          "description": "LED bench lamp",
          "quantity": 4,
          "unit_price": "32.50",
          "line_total": "130.00",
          "page": 1
        },
        {
          "sku": "NR-1010",
          "description": "Storage bin, 12 liter",
          "quantity": 16,
          "unit_price": "4.75",
          "line_total": "76.00",
          "page": 1
        },
        {
          "sku": "NR-1011",
          "description": "Letter clipboard",
          "quantity": 14,
          "unit_price": "2.85",
          "line_total": "39.90",
          "page": 1
        },
        {
          "sku": "NR-1012",
          "description": "Packing tape, 6 rolls",
          "quantity": 8,
          "unit_price": "9.60",
          "line_total": "76.80",
          "page": 1
        },
        {
          "sku": "NR-1013",
          "description": "Black permanent marker",
          "quantity": 30,
          "unit_price": "1.25",
          "line_total": "37.50",
          "page": 2
        },
        {
          "sku": "NR-1014",
          "description": "First aid refill kit",
          "quantity": 3,
          "unit_price": "18.40",
          "line_total": "55.20",
          "page": 2
        },
        {
          "sku": "NR-1015",
          "description": "Extension cord, 5 meter",
          "quantity": 6,
          "unit_price": "13.75",
          "line_total": "82.50",
          "page": 2
        },
        {
          "sku": "NR-1016",
          "description": "Large desk mat",
          "quantity": 5,
          "unit_price": "21.00",
          "line_total": "105.00",
          "page": 2
        },
        {
          "sku": "NR-1017",
          "description": "Two-step stool",
          "quantity": 2,
          "unit_price": "45.00",
          "line_total": "90.00",
          "page": 2
        },
        {
          "sku": "NR-1018",
          "description": "Silent wall clock",
          "quantity": 6,
          "unit_price": "14.50",
          "line_total": "87.00",
          "page": 2
        },
        {
          "sku": "NR-1019",
          "description": "Waste bin, 20 liter",
          "quantity": 8,
          "unit_price": "9.95",
          "line_total": "79.60",
          "page": 2
        },
        {
          "sku": "NR-1020",
          "description": "Hand soap, carton of 4",
          "quantity": 4,
          "unit_price": "12.80",
          "line_total": "51.20",
          "page": 2
        },
        {
          "sku": "NR-1021",
          "description": "Paper towel, carton",
          "quantity": 6,
          "unit_price": "15.20",
          "line_total": "91.20",
          "page": 2
        },
        {
          "sku": "NR-1022",
          "description": "Broom with dustpan",
          "quantity": 4,
          "unit_price": "11.45",
          "line_total": "45.80",
          "page": 2
        },
        {
          "sku": "NR-1023",
          "description": "Doorstop wedge",
          "quantity": 12,
          "unit_price": "2.15",
          "line_total": "25.80",
          "page": 2
        },
        {
          "sku": "NR-1024",
          "description": "Shelf label holder",
          "quantity": 20,
          "unit_price": "1.85",
          "line_total": "37.00",
          "page": 2
        },
        {
          "sku": "NR-1025",
          "description": "Key cabinet, 20 hooks",
          "quantity": 1,
          "unit_price": "36.00",
          "line_total": "36.00",
          "page": 3
        },
        {
          "sku": "NR-1026",
          "description": "Wet floor sign",
          "quantity": 5,
          "unit_price": "8.70",
          "line_total": "43.50",
          "page": 3
        },
        {
          "sku": "NR-1027",
          "description": "Batteries, AA pack of 20",
          "quantity": 9,
          "unit_price": "7.60",
          "line_total": "68.40",
          "page": 3
        },
        {
          "sku": "NR-1028",
          "description": "Utility knife",
          "quantity": 6,
          "unit_price": "4.35",
          "line_total": "26.10",
          "page": 3
        },
        {
          "sku": "NR-1029",
          "description": "Clear storage box",
          "quantity": 10,
          "unit_price": "3.90",
          "line_total": "39.00",
          "page": 3
        },
        {
          "sku": "NR-1030",
          "description": "Wall hook, pack of 6",
          "quantity": 8,
          "unit_price": "5.55",
          "line_total": "44.40",
          "page": 3
        }
      ],
      "order_total": {
        "value": "1989.60",
        "pages": [
          3
        ]
      }
    }
  ]
}
```
