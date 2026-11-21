from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
html = PAGE.read_text(encoding="utf-8")


def replace_once(pattern: str, replacement: str, source: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, source, count=1, flags=re.I | re.S)
    if count != 1:
        raise SystemExit(f"Expected exactly one match for {label}; found {count}. No changes committed.")
    return updated


html = replace_once(r'<html lang="en">', '<html lang="en-KE">', html, "html language")
html = replace_once(
    r'<title>[^<]*</title>',
    '<title>Printing Services in Nairobi, Kenya | Kazisafii Print &amp; Gifts</title>',
    html,
    "homepage title",
)
html = replace_once(
    r'<meta name="description" content="[^"]*">',
    '<meta name="description" content="Printing services and personalised gifts in Nairobi, Kenya. Shop business cards, flyers, banners, stickers, mugs, posters and custom gifts. Design online, pay with M-Pesa and track your order.">',
    html,
    "homepage description",
)

head_meta = '''
<link rel="canonical" href="https://kazisafii.co.ke/">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:title" content="Printing Services in Nairobi, Kenya | Kazisafii Print &amp; Gifts">
<meta property="og:description" content="Printing services and personalised gifts in Nairobi, Kenya. Shop business cards, flyers, banners, stickers, mugs, posters and custom gifts. Design online, pay with M-Pesa and track your order.">
<meta property="og:url" content="https://kazisafii.co.ke/">
<meta property="og:site_name" content="Kazisafii Print &amp; Gifts">
<meta property="og:locale" content="en_KE">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Printing Services in Nairobi | Kazisafii Print &amp; Gifts">
<meta name="twitter:description" content="Printing and personalised gifts in Nairobi. Browse products, design online and request a quote.">
'''
html = replace_once(
    r'(<meta name="description" content="[^"]*">)',
    r'\1' + head_meta,
    html,
    "homepage metadata insertion",
)

org_schema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": "https://kazisafii.co.ke/#organization",
    "name": "Kazisafii Print & Gifts",
    "url": "https://kazisafii.co.ke/",
    "description": "Online printing, personalised gifts and branded merchandise serving Nairobi and customers across Kenya.",
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
json_script = '<script type="application/ld+json">' + json.dumps(org_schema, ensure_ascii=False, indent=2) + '</script>\n'
html = replace_once(r'(</head>)', json_script + r'\1', html, "homepage JSON-LD insertion")

# Improve the accessible logo label; the artwork itself is intentionally left untouched.
html = html.replace('aria-label="Kazisafi home"', 'aria-label="Kazisafii Print and Gifts home"')
html = html.replace('alt="Kazisafi print and gifts"', 'alt="Kazisafii Print & Gifts logo"')
html = html.replace('© Kazisafi. All rights reserved.', '© Kazisafii Print & Gifts. All rights reserved.')

seo_section = '''<section class="sec seo-hub"><h2>Printing services and personalised gifts in Nairobi</h2><p>Kazisafii Print &amp; Gifts brings business printing, branded merchandise and personalised gifts together in one online shop. Browse the product pages below for current starting prices, minimum quantities and available options. We serve Nairobi and arrange delivery beyond Nairobi; confirm the final price and delivery details for your order.</p><div class="seo-links"><a href="/printing-services-nairobi/">Printing services in Nairobi</a><a href="/business-card-printing-nairobi/">Business card printing</a><a href="/flyer-printing-nairobi/">Flyer printing</a><a href="/banner-printing-nairobi/">Banner printing</a><a href="/roll-up-banner-printing-nairobi/">Roll-up banner printing</a><a href="/poster-printing-nairobi/">Poster printing</a><a href="/sticker-printing-nairobi/">Sticker and label printing</a><a href="/t-shirt-printing-nairobi/">Custom T-shirt printing</a><a href="/mug-printing-nairobi/">Mug printing</a><a href="/personalised-gifts-nairobi/">Personalised gifts</a><a href="/corporate-gifts-branded-merchandise-nairobi/">Corporate gifts and branded merchandise</a></div></section>\n'''
html = replace_once(
    r'(<section class="sec"><h2>Three easy ways to order</h2>)',
    seo_section + r'\1',
    html,
    "homepage service link hub",
)

css = '''
.seo-hub{max-width:1180px;margin:30px auto;padding:30px 24px;background:var(--soft);border-radius:18px}.seo-hub h2{margin:0 0 10px}.seo-hub>p{max-width:850px;color:var(--mut);margin:0 0 18px}.seo-links{display:grid;grid-template-columns:repeat(auto-fit,minmax(185px,1fr));gap:10px}.seo-links a{display:block;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;color:var(--ink);text-decoration:none;font-weight:650}.seo-links a:hover{border-color:var(--red);color:var(--red)}
'''
html = replace_once(r'(</style>)', css + r'\1', html, "homepage service hub styles")

PAGE.write_text(html, encoding="utf-8")
print(f"Homepage SEO updated ({len(html)} characters).")
