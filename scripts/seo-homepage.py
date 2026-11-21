from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
html = PAGE.read_text(encoding="utf-8")

# Keep customer-facing brand spelling consistent in WhatsApp and order templates.
html = re.sub(r'(?<![A-Za-z])Kazisafi(?![A-Za-z])', 'Kazisafii', html)


def replace_once(pattern: str, replacement: str, source: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, source, count=1, flags=re.I | re.S)
    if count != 1:
        raise SystemExit(f"Expected exactly one match for {label}; found {count}. No changes committed.")
    return updated


html = replace_once(r'<html lang="(?:en|en-KE)">', '<html lang="en-KE">', html, "html language")
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
if '<link rel="canonical" href="https://kazisafii.co.ke/">' not in html:
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
if '"@id": "https://kazisafii.co.ke/#organization"' not in html:
    html = replace_once(r'(</head>)', json_script + r'\1', html, "homepage JSON-LD insertion")

# Improve the accessible logo label; the artwork itself is intentionally left untouched.
html = html.replace('aria-label="Kazisafi home"', 'aria-label="Kazisafii Print and Gifts home"')
html = html.replace('alt="Kazisafi print and gifts"', 'alt="Kazisafii Print & Gifts logo"')
html = html.replace('© Kazisafi. All rights reserved.', '© Kazisafii Print & Gifts. All rights reserved.')

footer_links = '''<div class="seo-footer-links"><b>Printing &amp; gifts</b><a href="/printing-services-nairobi/">Printing services in Nairobi</a><a href="/business-card-printing-nairobi/">Business card printing</a><a href="/flyer-printing-nairobi/">Flyer printing</a><a href="/banner-printing-nairobi/">Banner printing</a><a href="/sticker-printing-nairobi/">Sticker printing</a><a href="/mug-printing-nairobi/">Mug printing</a><a href="/t-shirt-printing-nairobi/">T-shirt printing</a><a href="/roll-up-banner-printing-nairobi/">Roll-up banner printing</a><a href="/poster-printing-nairobi/">Poster printing</a><a href="/personalised-gifts-nairobi/">Personalised gifts</a><a href="/corporate-gifts-branded-merchandise-nairobi/">Corporate gifts</a><a href="/about-kazisafii/">About Kazisafii</a><a href="/printing-guides-nairobi/">Printing guides</a><a href="/print-ready-artwork-guide-nairobi/">Print-ready artwork checklist</a><a href="/business-card-finishes-guide-nairobi/">Business-card finishes guide</a><a href="/contact-kazisafii/">Contact Kazisafii</a></div>'''
# Rebuild the SEO footer block from a single canonical source. This also removes
# legacy placeholders and duplicate blocks from earlier deployments.
html = re.sub(
    r'\\1<a href="/printing-guides-nairobi/">[\s\S]*?<a href="/business-card-finishes-guide-nairobi/">Business-card finishes guide</a>',
    '',
    html,
    count=1,
)
html = re.sub(r'<div class="seo-footer-links">[\s\S]*?</div>', '', html)
html = replace_once(
    r'(<a href="#shop" onclick="G=-1">All products</a>)',
    lambda match: match.group(1) + footer_links,
    html,
    "rebuild single static footer service-link block",
)




# Provide a useful HTML fallback for visitors and crawlers that do not run JavaScript.
# The live shop app replaces this content when JavaScript is enabled.
noscript_home = '''<noscript><section class="nojs-home"><p class="eyebrow">Kazisafii Print &amp; Gifts · Nairobi, Kenya</p><h1>Printing services and personalised gifts in Nairobi</h1><p>Browse business cards, flyers, brochures, posters, banners, stickers, custom apparel, branded bags, packaging and personalised photo gifts. Kazisafii serves Nairobi and customers across Kenya, with online ordering, M-Pesa payment and delivery options.</p><p>Explore catalogue starting prices, product options and minimum quantities on the dedicated service pages, then contact the team to confirm your order.</p><div class="seo-links"><a href="/printing-services-nairobi/">Printing services in Nairobi</a><a href="/business-card-printing-nairobi/">Business card printing</a><a href="/flyer-printing-nairobi/">Flyer printing</a><a href="/banner-printing-nairobi/">Banner printing</a><a href="/custom-apparel-printing-nairobi/">Custom apparel printing</a><a href="/bags-and-packaging-printing-nairobi/">Branded bags and packaging</a><a href="/flyers-brochures-printing-nairobi/">Brochures and menus</a><a href="/banners-event-displays-printing-nairobi/">Event displays</a><a href="/photo-printing-personalised-photo-gifts-nairobi/">Photo printing and gifts</a><a href="/personalised-gifts-nairobi/">Personalised gifts</a><a href="/corporate-gifts-branded-merchandise-nairobi/">Corporate gifts</a><a href="/contact-kazisafii/">Contact Kazisafii</a></div><p>Call or WhatsApp <a href="tel:+254743288927">0743 288 927</a>.</p></section></noscript>'''
if 'class="nojs-home"' not in html:
    html = replace_once(r'(</main>)', lambda match: noscript_home + match.group(1), html, "insert no-JavaScript homepage fallback")

products_section = r'''<section class="sec" id="home-products"><h2>Shop printing &amp; personalised gifts</h2><p>Explore popular products from Kazi Safii. Choose an item to customise or order.</p><div class="grid">${IT.slice(0,12).map((x,i)=>card(x,i,1)).join('')}</div><p style="margin-top:22px"><a class="btn" href="#shop" onclick="G=-1;QF=''">View all products</a></p></section>'''
# Keep the homepage's approved visual structure, but make its products the first content below the header.
html = re.sub(r'<section class="sec" id="home-products">[\s\S]*?</section>', '', html, count=1)
product_start = r'(home:\(\)=>\{[\s\S]*?return' + re.escape(chr(96)) + r')(<div class="wrap"><div class="cats">)'
html = replace_once(
    product_start,
    lambda match: match.group(1) + products_section + match.group(2),
    html,
    "put featured products first on homepage",
)

seo_section = '''<section class="sec seo-hub"><h2>Printing services and personalised gifts in Nairobi</h2><p>Kazisafii Print &amp; Gifts brings business printing, branded merchandise and personalised gifts together in one online shop. Browse the product pages below for current starting prices, minimum quantities and available options. We serve Nairobi and arrange delivery beyond Nairobi; confirm the final price and delivery details for your order.</p><div class="seo-links"><a href="/printing-services-nairobi/">Printing services in Nairobi</a><a href="/business-card-printing-nairobi/">Business card printing</a><a href="/flyer-printing-nairobi/">Flyer printing</a><a href="/banner-printing-nairobi/">Banner printing</a><a href="/roll-up-banner-printing-nairobi/">Roll-up banner printing</a><a href="/poster-printing-nairobi/">Poster printing</a><a href="/sticker-printing-nairobi/">Sticker and label printing</a><a href="/t-shirt-printing-nairobi/">Custom T-shirt printing</a><a href="/mug-printing-nairobi/">Mug printing</a><a href="/personalised-gifts-nairobi/">Personalised gifts</a><a href="/corporate-gifts-branded-merchandise-nairobi/">Corporate gifts and branded merchandise</a></div></section>\\n'''
# Relocate the SEO links after all existing homepage sections.
html = re.sub(r'<section class="sec seo-hub">[\s\S]*?</section>\s*', '', html, flags=re.I)
home_end = r'(\$\{recentRow\(\)\})' + re.escape(chr(96)) + r'\},\s*shop:\(\)=>'
html = replace_once(
    home_end,
    lambda match: match.group(1) + seo_section + chr(96) + '},\nshop:()=>',
    html,
    "move homepage SEO link hub to the bottom",
)

css = '''
.seo-hub{max-width:1180px;margin:30px auto;padding:30px 24px;background:var(--soft);border-radius:18px}.seo-hub h2{margin:0 0 10px}.seo-hub>p{max-width:850px;color:var(--mut);margin:0 0 18px}.seo-links{display:grid;grid-template-columns:repeat(auto-fit,minmax(185px,1fr));gap:10px}.seo-links a{display:block;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;color:var(--ink);text-decoration:none;font-weight:650}.seo-links a:hover{border-color:var(--red);color:var(--red)}
.seo-footer-links{margin-top:12px;padding-top:10px;border-top:1px solid var(--line)}.seo-footer-links b{font-size:13px}.seo-footer-links a{font-size:12px;line-height:1.45}
.nojs-home{max-width:1100px;margin:30px auto;padding:28px 22px;background:var(--soft);border-radius:14px}.nojs-home h1{color:var(--ink);font-size:clamp(30px,5vw,48px);line-height:1.1;margin:10px 0 14px}.nojs-home p{max-width:78ch}.nojs-home .seo-links{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px;margin:18px 0}.nojs-home .seo-links a{background:var(--card);border:1px solid var(--line);padding:10px 12px;border-radius:9px;color:var(--ink);font-weight:650;text-decoration:none}
'''
if '.seo-hub{' not in html:
    html = replace_once(r'(</style>)', css + r'\1', html, "homepage service hub styles")

if re.search(r'(?<![A-Za-z])Kazisafi(?![A-Za-z])', html):
    raise SystemExit("Found an old customer-facing Kazisafi spelling in the homepage source.")
if html.count('class="nojs-home"') != 1:
    raise SystemExit(f"Expected exactly one no-JavaScript fallback; found {html.count('class=\"nojs-home\"')}.")
if html.count('class="seo-footer-links"') != 1:
    raise SystemExit(f"Expected exactly one static SEO footer block; found {html.count('class=\"seo-footer-links\"')}.")
# Apply the supplied double-i brand artwork to both header and footer logos.
logo_assets = """
<script>
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.lgi').forEach(function (img) {
    img.src = '/assets/kazisafii-logo.webp';
    img.alt = 'Kazisafii Print & Gifts logo';
  });
  document.querySelectorAll('.lgw').forEach(function (img) {
    img.src = '/assets/kazisafii-logo-white.webp';
    img.alt = 'Kazisafii Print & Gifts logo';
  });
});
</script>
"""
if "assets/kazisafii-logo.webp" not in html:
    html = replace_once(r'(</body>)', logo_assets + r'\1', html, "double-i logo asset script")

PAGE.write_text(html, encoding="utf-8")
print(f"Homepage SEO updated ({len(html)} characters); verified one static fallback and one SEO footer block.")
