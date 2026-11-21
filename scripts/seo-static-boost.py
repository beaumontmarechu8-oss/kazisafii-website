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
if 'class="kz-seo-bottom"' not in html:
    marker = "</main>\n<footer>"
    if html.count(marker) != 1:
        raise SystemExit(f"Expected one homepage/footer boundary, found {html.count(marker)}. No changes written.")
    html = html.replace(marker, "</main>\n" + seo_section + "<footer>", 1)

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
