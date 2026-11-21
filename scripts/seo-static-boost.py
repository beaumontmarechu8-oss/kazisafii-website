from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
html = PAGE.read_text(encoding="utf-8")

TITLE = "Printing Services in Nairobi, Kenya | Kazisafii"
DESCRIPTION = "Printing services in Nairobi: business cards, flyers, banners, stickers, apparel and personalised gifts. Browse products, pay by M-Pesa and request a quote."

html = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", html, count=1, flags=re.I | re.S)
html = re.sub(
    r'<meta\s+name=["\']description["\']\s+content=["\'][^"\']*["\']\s*/?>',
    f'<meta name="description" content="{DESCRIPTION}">',
    html,
    count=1,
    flags=re.I,
)

head_meta = f'''
<link rel="canonical" href="https://kazisafii.co.ke/">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESCRIPTION}">
<meta property="og:url" content="https://kazisafii.co.ke/">
<meta property="og:site_name" content="Kazisafii Print &amp; Gifts">
<meta property="og:locale" content="en_KE">
<meta property="og:image" content="https://kazisafii.co.ke/assets/products/29.webp">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESCRIPTION}">
<meta name="twitter:image" content="https://kazisafii.co.ke/assets/products/29.webp">
'''
if 'rel="canonical" href="https://kazisafii.co.ke/"' not in html:
    html = html.replace("</head>", head_meta + "</head>", 1)

organization = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": "https://kazisafii.co.ke/#organization",
    "name": "Kazisafii Print & Gifts",
    "url": "https://kazisafii.co.ke/",
    "description": "Printing services, branded merchandise and personalised gifts serving Nairobi and customers across Kenya.",
    "telephone": "+254743288927",
    "areaServed": [
        {"@type": "City", "name": "Nairobi"},
        {"@type": "Country", "name": "Kenya"},
    ],
    "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+254743288927",
        "contactType": "customer service",
        "areaServed": "KE",
        "availableLanguage": ["English"],
    },
}
if '"@id": "https://kazisafii.co.ke/#organization"' not in html:
    schema = '<script type="application/ld+json">' + json.dumps(organization, ensure_ascii=False) + '</script>\n'
    html = html.replace("</head>", schema + "</head>", 1)

html = html.replace('alt="Kazisafi print and gifts"', 'alt="Kazisafii Print &amp; Gifts logo"')
html = html.replace('aria-label="Kazisafi home"', 'aria-label="Kazisafii Print and Gifts home"')
html = html.replace("<h1>Put your heart on it.</h1>", "<h2>Put your heart on it.</h2>")
html = html.replace(".xh h1{font-size:clamp(44px,6.4vw,92px);line-height:.93;letter-spacing:-.045em;margin:0 0 18px;color:#fff}", ".xh h1,.xh h2{font-size:clamp(44px,6.4vw,92px);line-height:.93;letter-spacing:-.045em;margin:0 0 18px;color:#fff}")

seo_section = '''
<section class="kz-seo-bottom" aria-labelledby="kz-printing-services-heading">
  <h1 id="kz-printing-services-heading">Printing services and personalised gifts in Nairobi</h1>
  <p>Kazisafii Print &amp; Gifts brings everyday business printing, large-format displays, branded merchandise and personalised gifts together in one online shop. Browse product information, compare available options and contact the team for a quotation. Orders can be paid for using M-Pesa, with collection or delivery arrangements confirmed with the team.</p>
  <div class="kz-seo-links">
    <a href="/printing-services-nairobi/">All printing services in Nairobi</a>
    <a href="/business-card-printing-nairobi/">Business card printing</a>
    <a href="/flyer-printing-nairobi/">Flyer printing</a>
    <a href="/banner-printing-nairobi/">Banner and display printing</a>
    <a href="/sticker-printing-nairobi/">Sticker and label printing</a>
    <a href="/t-shirt-printing-nairobi/">Custom T-shirt printing</a>
    <a href="/mug-printing-nairobi/">Mug printing</a>
    <a href="/photo-printing-personalised-photo-gifts-nairobi/">Photo printing and gifts</a>
    <a href="/bags-and-packaging-printing-nairobi/">Branded bags and packaging</a>
    <a href="/corporate-gifts-branded-merchandise-nairobi/">Corporate gifts and merchandise</a>
    <a href="/printing-portfolio-nairobi/">View our printing portfolio and product photos</a>
  </div>
  <p class="kz-seo-contact">Need help choosing a product? <a href="https://wa.me/254743288927">WhatsApp Kazisafii on 0743 288 927</a>.</p>
</section>
'''
# Always place the crawlable service section inside main, immediately before the footer.
html = re.sub(r'\n<section class="kz-seo-bottom"[\s\S]*?</section>\s*', '', html, count=1)
marker = "</main>\n<footer>"
if html.count(marker) != 1:
    raise SystemExit(f"Expected one homepage/footer boundary, found {html.count(marker)}. No changes written.")
html = html.replace(marker, seo_section + "</main>\n<footer>", 1)

style = '''
.kz-seo-bottom{max-width:1100px;margin:12px auto 34px;padding:26px 18px 12px;border-top:2px solid var(--line);color:var(--ink)}
.kz-seo-bottom h1,.kz-seo-bottom h2{margin:0 0 12px;font-size:clamp(24px,4vw,32px)}
.kz-seo-bottom p{max-width:900px;color:var(--mut);margin:0 0 16px;line-height:1.65}
.kz-seo-links{display:grid;grid-template-columns:repeat(auto-fit,minmax(185px,1fr));gap:9px}
.kz-seo-links a{display:block;padding:11px 13px;border:1px solid var(--line);border-radius:10px;color:var(--ink);background:var(--soft);font-weight:650;text-decoration:none}
.kz-seo-links a:hover{border-color:var(--red);color:var(--red)}
.kz-seo-contact{margin-top:18px!important}
'''
if '.kz-seo-bottom{' not in html:
    html = html.replace("</style>", style + "</style>", 1)

if html.count('class="kz-seo-bottom"') != 1:
    raise SystemExit("SEO homepage section validation failed.")
if 'rel="canonical" href="https://kazisafii.co.ke/"' not in html:
    raise SystemExit("Canonical URL is missing after homepage update.")
PAGE.write_text(html, encoding="utf-8")
print(f"Updated homepage SEO head and appended crawlable printing-services content ({len(html)} characters).")

# Re-run the homepage SEO build after adding this workflow to the default branch.


# Add genuine catalogue photography to each matching service page.
SERVICE_PHOTO_PAGES = {
    "printing-services-nairobi": {
        "heading": "See products from the Kazisafii print catalogue",
        "items": [
            ("business-card-spot-uv-printing-nairobi.webp", "Business card printing in Nairobi"),
            ("flyer-brochure-printing-nairobi.webp", "Flyer and brochure printing in Nairobi"),
            ("banner-printing-nairobi.webp", "Large-format banner printing in Nairobi"),
            ("vinyl-sticker-printing-nairobi.webp", "Custom vinyl sticker printing in Nairobi"),
        ],
    },
    "business-card-printing-nairobi": {
        "heading": "Business card printing examples",
        "items": [("business-card-spot-uv-printing-nairobi.webp", "Printed business cards with premium Spot UV finish")],
    },
    "banner-printing-nairobi": {
        "heading": "Banner and display printing examples",
        "items": [
            ("banner-printing-nairobi.webp", "Custom printed banner"),
            ("x-banner-printing-nairobi.webp", "X-banner display printing"),
            ("roll-up-banner-printing-nairobi.webp", "Roll-up banner printing"),
        ],
    },
    "flyer-printing-nairobi": {
        "heading": "Flyer and promotional print examples",
        "items": [
            ("flyer-brochure-printing-nairobi.webp", "Printed flyers and brochures"),
            ("menu-printing-nairobi.webp", "Custom printed menus"),
        ],
    },
    "sticker-printing-nairobi": {
        "heading": "Sticker and label printing examples",
        "items": [
            ("vinyl-sticker-printing-nairobi.webp", "Custom vinyl sticker printing"),
            ("label-sticker-printing-nairobi.webp", "Printed product label stickers"),
            ("car-decal-printing-nairobi.webp", "Custom car decal printing"),
        ],
    },
    "roll-up-banner-printing-nairobi": {
        "heading": "Portable display banner examples",
        "items": [
            ("roll-up-banner-printing-nairobi.webp", "Printed roll-up banner display"),
            ("x-banner-printing-nairobi.webp", "Printed X-banner display"),
            ("backdrop-banner-printing-nairobi.webp", "Custom event backdrop banner"),
        ],
    },
    "t-shirt-printing-nairobi": {
        "heading": "Custom apparel printing examples",
        "items": [
            ("custom-t-shirt-printing-nairobi.webp", "Custom printed T-shirt"),
            ("polo-shirt-printing-nairobi.webp", "Custom branded polo shirt"),
            ("hoodie-printing-nairobi.webp", "Custom printed hoodie"),
        ],
    },
    "mug-printing-nairobi": {
        "heading": "Custom mug and drinkware examples",
        "items": [
            ("custom-mug-printing-nairobi.webp", "Custom printed ceramic mug"),
            ("enamel-mug-printing-nairobi.webp", "Custom enamel mug"),
            ("thermal-travel-mug-printing-nairobi.webp", "Custom thermal travel mug"),
        ],
    },
    "photo-printing-personalised-photo-gifts-nairobi": {
        "heading": "Photo printing and personalised gift examples",
        "items": [
            ("photo-printing-nairobi.webp", "Printed photo prints"),
            ("mounted-photo-printing-nairobi.webp", "Mounted photo printing"),
            ("photo-framing-nairobi.webp", "Custom photo framing"),
            ("canvas-printing-nairobi.webp", "Canvas photo printing"),
        ],
    },
    "personalised-gifts-nairobi": {
        "heading": "Personalised gift ideas from the catalogue",
        "items": [
            ("custom-mug-printing-nairobi.webp", "Personalised photo and branded mugs"),
            ("custom-water-bottle-printing-nairobi.webp", "Custom printed water bottles"),
            ("gift-voucher-printing-nairobi.webp", "Printed gift vouchers"),
            ("photo-printing-nairobi.webp", "Photo prints and gifts"),
        ],
    },
    "corporate-gifts-branded-merchandise-nairobi": {
        "heading": "Branded merchandise and corporate gift examples",
        "items": [
            ("branded-tote-bag-printing-nairobi.webp", "Branded tote bag"),
            ("custom-cap-printing-nairobi.webp", "Custom branded caps"),
            ("custom-mug-printing-nairobi.webp", "Custom printed mugs"),
            ("custom-water-bottle-printing-nairobi.webp", "Branded water bottles"),
        ],
    },
    "bags-and-packaging-printing-nairobi": {
        "heading": "Branded bags and packaging examples",
        "items": [
            ("branded-tote-bag-printing-nairobi.webp", "Custom branded tote bags"),
            ("jute-bag-printing-nairobi.webp", "Branded jute bags"),
            ("kraft-bag-printing-nairobi.webp", "Printed kraft bags"),
            ("custom-packaging-box-printing-nairobi.webp", "Custom printed packaging boxes"),
        ],
    },
    "banners-event-displays-printing-nairobi": {
        "heading": "Event display and banner examples",
        "items": [
            ("x-banner-printing-nairobi.webp", "X-banner display printing"),
            ("roll-up-banner-printing-nairobi.webp", "Roll-up banner printing"),
            ("teardrop-banner-printing-nairobi.webp", "Tear drop banner printing"),
            ("pop-up-banner-printing-nairobi.webp", "Pop-up banner display"),
            ("backdrop-banner-printing-nairobi.webp", "Printed event backdrop"),
        ],
    },
    "flyers-brochures-printing-nairobi": {
        "heading": "Flyers, brochures and promotional print examples",
        "items": [
            ("flyer-brochure-printing-nairobi.webp", "Printed flyers and brochures"),
            ("menu-printing-nairobi.webp", "Custom printed menus"),
            ("funeral-program-printing-nairobi.webp", "Printed funeral programmes"),
            ("booklet-document-printing-nairobi.webp", "Booklet and document printing"),
        ],
    },
    "custom-apparel-printing-nairobi": {
        "heading": "Custom apparel and workwear examples",
        "items": [
            ("custom-t-shirt-printing-nairobi.webp", "Custom printed T-shirts"),
            ("polo-shirt-printing-nairobi.webp", "Custom branded polo shirts"),
            ("hoodie-printing-nairobi.webp", "Custom printed hoodies"),
            ("custom-jersey-printing-nairobi.webp", "Custom printed sports jerseys"),
            ("reflector-jacket-printing-nairobi.webp", "Custom reflector jackets"),
        ],
    },
}

PHOTO_STYLE = """
.service-photo-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:16px;margin:20px 0}
.service-photo{margin:0;background:#fff;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.service-photo img{display:block;width:100%;aspect-ratio:4/3;object-fit:contain;background:#fff;padding:10px}
.service-photo figcaption{padding:10px 13px;font-size:.92rem;color:var(--ink)}
.service-photo-more{margin-top:10px;font-weight:700}
"""

for slug, config in SERVICE_PHOTO_PAGES.items():
    service_file = ROOT / slug / "index.html"
    if not service_file.exists():
        raise SystemExit(f"Expected service page is missing: {service_file}")
    page_html = service_file.read_text(encoding="utf-8")
    if 'class="service-photo-grid"' not in page_html:
        hero_start = page_html.find('class="hero"')
        section_start = page_html.find("<section", hero_start)
        if hero_start < 0 or section_start < 0:
            raise SystemExit(f"Could not find hero and first section in {slug}")
        figures = []
        for filename, alt_text in config["items"]:
            image_url = f"/assets/printing-photos/{filename}"
            figures.append(
                f'<figure class="service-photo"><img src="{image_url}" '
                f'alt="{alt_text}" loading="lazy" decoding="async" width="720" height="540">'
                f'<figcaption>{alt_text}</figcaption></figure>'
            )
        photo_section = (
            f'<section class="service-photo-section" aria-label="{config["heading"]}">'
            f'<h2>{config["heading"]}</h2>'
            '<p>Browse actual product examples from the Kazisafii catalogue. '
            'Open the full portfolio to compare more print and gift products.</p>'
            '<div class="service-photo-grid">' + "\n".join(figures) + '</div>'
            '<p class="service-photo-more"><a href="/printing-portfolio-nairobi/">'
            'View the full Kazisafii printing and product photo portfolio</a></p>'
            '</section>\n'
        )
        page_html = page_html[:section_start] + photo_section + page_html[section_start:]
    if ".service-photo-grid{" not in page_html:
        if "</style>" not in page_html:
            raise SystemExit(f"Could not find style block in {slug}")
        page_html = page_html.replace("</style>", PHOTO_STYLE + "</style>", 1)
    og_image = f"https://kazisafii.co.ke/assets/printing-photos/{config['items'][0][0]}"
    if 'property="og:image"' not in page_html:
        social_meta = (
            f'<meta property="og:image" content="{og_image}">\n'
            f'<meta property="og:image:alt" content="{config["items"][0][1]}">\n'
            '<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:image" content="{og_image}">\n'
        )
        if "</head>" not in page_html:
            raise SystemExit(f"Could not find closing head tag in {slug}")
        page_html = page_html.replace("</head>", social_meta + "</head>", 1)
    else:
        page_html = re.sub(
            r'<meta\s+property=["\']og:image["\']\s+content=["\'][^"\']*["\']\s*/?>',
            f'<meta property="og:image" content="{og_image}">',
            page_html,
            count=1,
            flags=re.I,
        )
    if page_html.count('class="service-photo-grid"') != 1:
        raise SystemExit(f"Service photo section validation failed: {slug}")
    if len(re.findall(r"<h1\b", page_html, flags=re.I)) != 1:
        raise SystemExit(f"Unexpected H1 count after photo insertion: {slug}")
    service_file.write_text(page_html, encoding="utf-8")
    print(f"Added {len(config['items'])} relevant product photos to {slug}")

