from __future__ import annotations

import base64
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / ".site-build-source"
PRODUCT_IMAGES = ROOT / "assets" / "products"

required = ["index.html", "styles.css", "app.js", "products.js", "kazisafii-logo.svg"]
for name in required:
    path = SOURCE / name
    if not path.is_file():
        raise SystemExit(f"Missing required rebuild source: {path}")

# The previous homepage contains the original product photo data as embedded WebP.
# Extract only the 46 catalogue images before replacing that large legacy homepage.
legacy_home = ROOT / "index.html"
legacy_html = legacy_home.read_text(encoding="utf-8")
image_payloads = re.findall(r"data:image/webp;base64,([A-Za-z0-9+/=]+)", legacy_html)
if len(image_payloads) < 50:
    raise SystemExit(f"Expected at least 50 embedded WebP images in the legacy homepage; found {len(image_payloads)}. No homepage replacement performed.")

PRODUCT_IMAGES.mkdir(parents=True, exist_ok=True)
for index, payload in enumerate(image_payloads[4:50]):
    image = base64.b64decode(payload, validate=True)
    if len(image) < 16 or image[:4] != b"RIFF" or image[8:12] != b"WEBP":
        raise SystemExit(f"Embedded image {index + 4} is not a valid WebP. No homepage replacement performed.")
    (PRODUCT_IMAGES / f"{index:02d}.webp").write_bytes(image)

# Copy the new product-first site files into the Render static-site root.
for name in ["index.html", "styles.css", "app.js", "products.js"]:
    (ROOT / name).write_bytes((SOURCE / name).read_bytes())
(ROOT / "assets" / "kazisafii-logo.svg").write_bytes((SOURCE / "kazisafii-logo.svg").read_bytes())

# Keep older SEO landing pages reachable while removing statements that imply
# unverified catalogue prices are fixed or guaranteed.
price_phrases = [
    (re.compile(r"Prices shown in the catalogue are starting prices, not a final quote\.", re.I), "Final pricing is confirmed against your exact specifications before production."),
    (re.compile(r"Prices shown are starting prices\.\s*Final costs[^<.]*\.", re.I), "Final pricing is confirmed against your exact specifications before production."),
    (re.compile(r"Prices shown are starting prices\.", re.I), "Final pricing is confirmed against your exact specifications before production."),
    (re.compile(r"The catalogue shows starting prices\.", re.I), "The catalogue helps you select products and request a tailored quote."),
    (re.compile(r"The catalogue lists starting prices where available\.", re.I), "The catalogue helps you select products and request a tailored quote."),
    (re.compile(r"catalogue for products and starting prices", re.I), "catalogue for products and request a tailored quote"),
]
for page in ROOT.rglob("index.html"):
    if SOURCE in page.parents or ".git" in page.parts or "node_modules" in page.parts:
        continue
    text = page.read_text(encoding="utf-8")
    updated = text
    for pattern, replacement in price_phrases:
        updated = pattern.sub(replacement, updated)
    if updated != text:
        page.write_text(updated, encoding="utf-8")

# Validate product data and ensure every referenced product image now exists.
product_text = (ROOT / "products.js").read_text(encoding="utf-8")
match = re.search(r"window\.KAZISAFI_PRODUCTS\s*=\s*(\[.*?\]);", product_text, re.S)
if not match:
    raise SystemExit("Could not parse the product catalogue JSON.")
products = json.loads(match.group(1))
for item in products:
    image = item.get("image")
    if image and not (ROOT / image).is_file():
        raise SystemExit(f"Missing product image for {item.get('name')}: {image}")

home = (ROOT / "index.html").read_text(encoding="utf-8")
if not (home.index('id="catalogue"') < home.index('id="services"')):
    raise SystemExit("Homepage order check failed: the product catalogue must appear before services.")
if not (ROOT / "assets" / "kazisafii-logo.svg").is_file():
    raise SystemExit("The approved Kazisafii logo is missing.")

# Build a sitemap from the pages that actually exist, retaining all existing
# landing pages while adding the latest product-first site's pages.
urls: set[str] = {"https://kazisafii.co.ke/"}
for page in ROOT.rglob("index.html"):
    if page == ROOT / "index.html" or SOURCE in page.parents or ".git" in page.parts:
        continue
    relative = page.parent.relative_to(ROOT).as_posix()
    if relative.startswith(("assets/", "scripts/", ".site-build-source/", ".github/")):
        continue
    canonical = f"https://kazisafii.co.ke/{relative.strip('/')}/"
    page_text = page.read_text(encoding="utf-8")
    canonical_match = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', page_text, re.I)
    if canonical_match:
        canonical = canonical_match.group(1)
    urls.add(canonical)

now = datetime.now(timezone.utc).date().isoformat()
ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("", ns)
urlset = ET.Element(f"{{{ns}}}urlset")
for url in sorted(urls):
    entry = ET.SubElement(urlset, f"{{{ns}}}url")
    ET.SubElement(entry, f"{{{ns}}}loc").text = url
    ET.SubElement(entry, f"{{{ns}}}lastmod").text = now
    ET.SubElement(entry, f"{{{ns}}}changefreq").text = "weekly" if url.endswith("/") and url == "https://kazisafii.co.ke/" else "monthly"
    ET.SubElement(entry, f"{{{ns}}}priority").text = "1.0" if url == "https://kazisafii.co.ke/" else "0.7"
ET.indent(urlset, space="  ")
ET.ElementTree(urlset).write(ROOT / "sitemap.xml", encoding="utf-8", xml_declaration=True)

(ROOT / "robots.txt").write_text(
    "User-agent: *\nAllow: /\n\nSitemap: https://kazisafii.co.ke/sitemap.xml\n",
    encoding="utf-8",
)

print(f"Built product-first homepage with {len(products)} products, {len(set(p['category'] for p in products))} categories, 46 verified WebP photos and {len(urls)} sitemap URLs.")