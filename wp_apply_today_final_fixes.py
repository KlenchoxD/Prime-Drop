import html
import json
import os
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import requests

BASE = "https://primedropelite.com"
USER = os.environ["PD_WP_USER"]
PASS = os.environ["PD_WP_PASS"]
TERMS_PAGE_ID = 751

MARKER_START = "/* PRIME_DROP_TODAY_FINAL_FIXES_START */"
MARKER_END = "/* PRIME_DROP_TODAY_FINAL_FIXES_END */"

TERMS_TEXT = """Welcome to Prime Drop!

These terms and conditions outline the rules and regulations for the use of Prime Drop's Website, located at https://primedropelite.com.

By accessing this website, we assume you accept these terms and conditions. Do not continue to use Prime Drop if you do not agree to take all of the terms and conditions stated on this page.

Cookies:
The website uses cookies to help personalize your online experience. By accessing Prime Drop, you agreed to use the required cookies.

A cookie is a text file that is placed on your hard disk by a web page server. Cookies cannot be used to run programs or deliver viruses to your computer. Cookies are uniquely assigned to you and can only be read by a web server in the domain that issued the cookie to you.

We may use cookies to collect, store, and track information for statistical or marketing purposes to operate our website. You have the ability to accept or decline optional Cookies. There are some required Cookies that are necessary for the operation of our website. These cookies do not require your consent as they always work. Please keep in mind that by accepting required Cookies, you also accept third-party Cookies, which might be used via third-party provided services if you use such services on our website, for example, a video display window provided by third parties and integrated into our website.

License:
Unless otherwise stated, Prime Drop and/or its licensors own the intellectual property rights for all material on Prime Drop. All intellectual property rights are reserved. You may access this from Prime Drop for your own personal use subjected to restrictions set in these terms and conditions.

You must not:

Copy or republish material from Prime Drop

Sell, rent, or sub-license material from Prime Drop

Reproduce, duplicate or copy material from Prime Drop

Redistribute content from Prime Drop

This Agreement shall begin on the date hereof.

Parts of this website offer users an opportunity to post and exchange opinions and information in certain areas of the website. Prime Drop does not filter, edit, publish or review Comments before their presence on the website. Comments do not reflect the views and opinions of Prime Drop, its agents, and/or affiliates. Comments reflect the views and opinions of the person who posts their views and opinions. To the extent permitted by applicable laws, Prime Drop shall not be liable for the Comments or any liability, damages, or expenses caused and/or suffered as a result of any use of and/or posting of and/or appearance of the Comments on this website.

Prime Drop reserves the right to monitor all Comments and remove any Comments that can be considered inappropriate, offensive, or causes breach of these Terms and Conditions.

You warrant and represent that:

You are entitled to post the Comments on our website and have all necessary licenses and consents to do so;

The Comments do not invade any intellectual property right, including without limitation copyright, patent, or trademark of any third party;

The Comments do not contain any defamatory, libelous, offensive, indecent, or otherwise unlawful material, which is an invasion of privacy.

The Comments will not be used to solicit or promote business or custom or present commercial activities or unlawful activity.

You hereby grant Prime Drop a non-exclusive license to use, reproduce, edit and authorize others to use, reproduce and edit any of your Comments in any and all forms, formats, or media.

Hyperlinking to our Content:
The following organizations may link to our Website without prior written approval:

Government agencies;

Search engines;

News organizations;

Online directory distributors may link to our Website in the same manner as they hyperlink to the Websites of other listed businesses; and

System-wide Accredited Businesses except soliciting non-profit organizations, charity shopping malls, and charity fundraising groups which may not hyperlink to our Web site.

These organizations may link to our home page, to publications, or to other Website information so long as the link: (a) is not in any way deceptive; (b) does not falsely imply sponsorship, endorsement, or approval of the linking party and its products and/or services; and (c) fits within the context of the linking party's site.

We may consider and approve other link requests from the following types of organizations:

Commonly-known consumer and/or business information sources;

Dot.com community sites;

Associations or other groups representing charities;

Online directory distributors;

Internet portals;

Accounting, law, and consulting firms; and

Educational institutions and trade associations.

We will approve link requests from these organizations if we decide that: (a) the link would not make us look unfavorably to ourselves or to our accredited businesses; (b) the organization does not have any negative records with us; (c) the benefit to us from the visibility of the hyperlink compensates the absence of Prime Drop; and (d) the link is in the context of general resource information.

These organizations may link to our home page so long as the link: (a) is not in any way deceptive; (b) does not falsely imply sponsorship, endorsement, or approval of the linking party and its products or services; and (c) fits within the context of the linking party's site.

If you are one of the organizations listed in paragraph 2 above and are interested in linking to our website, you must inform us by sending an e-mail to Prime Drop. Please include your name, your organization name, contact information as well as the URL of your site, a list of any URLs from which you intend to link to our Website, and a list of the URLs on our site to which you would like to link. Wait 2-3 weeks for a response.

Approved organizations may hyperlink to our Website as follows:

By use of our corporate name; or

By use of the uniform resource locator being linked to; or

Using any other description of our Website being linked to that makes sense within the context and format of content on the linking party's site.

No use of Prime Drop's logo or other artwork will be allowed for linking absent a trademark license agreement.

Content Liability:
We shall not be held responsible for any content that appears on your Website. You agree to protect and defend us against all claims that are raised on your Website. No link(s) should appear on any Website that may be interpreted as libelous, obscene, or criminal, or which infringes, otherwise violates, or advocates the infringement or other violation of, any third party rights.

Reservation of Rights:
We reserve the right to request that you remove all links or any particular link to our Website. You approve to immediately remove all links to our Website upon request. We also reserve the right to amend these terms and conditions and its linking policy at any time. By continuously linking to our Website, you agree to be bound to and follow these linking terms and conditions.

Removal of links from our website:
If you find any link on our Website that is offensive for any reason, you are free to contact and inform us at any moment. We will consider requests to remove links, but we are not obligated to or so or to respond to you directly.

We do not ensure that the information on this website is correct. We do not warrant its completeness or accuracy, nor do we promise to ensure that the website remains available or that the material on the website is kept up to date.

Disclaimer:
To the maximum extent permitted by applicable law, we exclude all representations, warranties, and conditions relating to our website and the use of this website. Nothing in this disclaimer will:

Limit or exclude our or your liability for death or personal injury;

Limit or exclude our or your liability for fraud or fraudulent misrepresentation;

Limit any of our or your liabilities in any way that is not permitted under applicable law; or

Exclude any of our or your liabilities that may not be excluded under applicable law.

The limitations and prohibitions of liability set in this Section and elsewhere in this disclaimer: (a) are subject to the preceding paragraph; and (b) govern all liabilities arising under the disclaimer, including liabilities arising in contract, in tort, and for breach of statutory duty.

As long as the website and the information and services on the website are provided free of charge, we will not be liable for any loss or damage of any nature."""

FUNCTIONS_BLOCK = r"""
/* PRIME_DROP_TODAY_FINAL_FIXES_START */
add_action('wp_footer', function() {
    ?>
    <style id="prime-drop-today-final-fixes-css">
    /* Orden por defecto: opciones legibles al hover/seleccion */
    body.page-id-547 select.orderby,
    body.page-id-547 .woocommerce-ordering select,
    body.woocommerce-shop select.orderby,
    body.tax-product_cat select.orderby {
      color: #ffffff !important;
    }

    body.page-id-547 select.orderby option,
    body.page-id-547 .woocommerce-ordering select option,
    body.woocommerce-shop select.orderby option,
    body.tax-product_cat select.orderby option {
      background: #ffffff !important;
      color: #000000 !important;
    }

    body.page-id-547 select.orderby option:hover,
    body.page-id-547 select.orderby option:focus,
    body.page-id-547 select.orderby option:checked,
    body.woocommerce-shop select.orderby option:hover,
    body.woocommerce-shop select.orderby option:checked,
    body.tax-product_cat select.orderby option:hover,
    body.tax-product_cat select.orderby option:checked {
      background: #000000 !important;
      color: #ffffff !important;
    }

    body.page-id-547 .select2-container--default .select2-results__option--highlighted[aria-selected],
    body.woocommerce-shop .select2-container--default .select2-results__option--highlighted[aria-selected],
    body.tax-product_cat .select2-container--default .select2-results__option--highlighted[aria-selected] {
      background: #000000 !important;
      color: #ffffff !important;
    }

    /* Reseñas antes de productos relacionados */
    .pd-product-reviews-preview {
      margin: 42px auto 26px !important;
      padding: 28px 30px !important;
      border-top: 1px solid #eeeeee !important;
      border-bottom: 1px solid #eeeeee !important;
      max-width: 1180px !important;
      display: grid !important;
      grid-template-columns: minmax(0, 1fr) auto !important;
      align-items: center !important;
      gap: 20px !important;
      background: #ffffff !important;
    }

    .pd-product-reviews-preview h2 {
      margin: 0 0 8px !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 28px !important;
      line-height: 1.1 !important;
      color: #000000 !important;
    }

    .pd-product-reviews-preview p {
      margin: 0 !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 14px !important;
      line-height: 1.55 !important;
      color: #333333 !important;
      max-width: 620px !important;
    }

    .pd-product-review-stars {
      display: flex !important;
      align-items: center !important;
      gap: 4px !important;
      font-size: 18px !important;
      line-height: 1 !important;
      letter-spacing: 2px !important;
      color: #000000 !important;
      margin-bottom: 10px !important;
    }

    .pd-product-review-note {
      text-align: right !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      font-size: 12px !important;
      font-weight: 800 !important;
      letter-spacing: 1.5px !important;
      text-transform: uppercase !important;
      color: #000000 !important;
      white-space: nowrap !important;
    }

    @media (max-width: 768px) {
      .pd-product-reviews-preview {
        grid-template-columns: 1fr !important;
        margin: 34px 18px 24px !important;
        padding: 24px 0 !important;
      }

      .pd-product-review-note {
        text-align: left !important;
        white-space: normal !important;
      }
    }

    /* Terminos y condiciones: lectura limpia */
    body.page-id-751 .entry-content,
    body.page-id-751 .ct-container-full .entry-content {
      max-width: 920px !important;
      margin-left: auto !important;
      margin-right: auto !important;
      padding: 42px 20px 70px !important;
      font-family: "Roboto Serif", Georgia, serif !important;
      color: #111111 !important;
    }

    body.page-id-751 .entry-content p {
      font-size: 15px !important;
      line-height: 1.75 !important;
      margin: 0 0 16px !important;
    }
    </style>

    <script id="prime-drop-today-final-fixes-js">
    (function() {
      var brandItems = [
        ['TODOS LOS BOLSOS', '/bolsos/'],
        ['KARL LAGERFELD', '/product-category/karl-lagerfeld/'],
        ['MICHAEL KORS', '/product-category/michael-kors/'],
        ['STEVE MADDEN', '/product-category/steve-madden/'],
        ['TOMMY HILFIGER', '/product-category/tommy-hilfiger/']
      ];

      function brandListHtml() {
        return brandItems.map(function(item) {
          return '<li><a href="' + item[1] + '"' + (item[0] === 'TODOS LOS BOLSOS' ? ' data-pd-all-bags="1"' : '') + '>' + item[0] + '</a></li>';
        }).join('');
      }

      function fixBolsosSubmenus() {
        document.querySelectorAll('.pd-bolsos-menu-parent').forEach(function(li) {
          var submenu = li.querySelector(':scope > .pd-bolsos-submenu');
          if (!submenu) return;
          if (submenu.dataset.pdBrandsOnly === '1') return;
          submenu.innerHTML = brandListHtml();
          submenu.dataset.pdBrandsOnly = '1';
        });
      }

      function fixBrandFilter() {
        if (!document.body.classList.contains('page-id-547')) return;
        var filter = document.querySelector('.pd-brand-filter');
        if (!filter || filter.dataset.pdBrandsOnly === '1') return;
        filter.innerHTML = brandItems.map(function(item) {
          return '<a href="' + item[1] + '">' + item[0] + '</a>';
        }).join('');
        filter.dataset.pdBrandsOnly = '1';
      }

      function run() {
        fixBolsosSubmenus();
        fixBrandFilter();
      }

      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', run);
      } else {
        run();
      }
      window.addEventListener('load', run);
      document.addEventListener('click', function(){ setTimeout(run, 120); }, true);
      new MutationObserver(run).observe(document.documentElement, { childList: true, subtree: true });
    })();
    </script>
    <?php
}, 10120);

add_action('woocommerce_after_single_product_summary', function() {
    if (!function_exists('is_product') || !is_product()) {
        return;
    }
    echo '<section class="pd-product-reviews-preview" aria-label="Reseñas de clientes">';
    echo '<div>';
    echo '<div class="pd-product-review-stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</div>';
    echo '<h2>Reseñas de clientes</h2>';
    echo '<p>Aún no hay reseñas publicadas para este bolso. Cuando completes tu compra, podrás compartir tu experiencia y ayudar a otras clientas a elegir mejor.</p>';
    echo '</div>';
    echo '<div class="pd-product-review-note">Opiniones verificadas</div>';
    echo '</section>';
}, 19);
/* PRIME_DROP_TODAY_FINAL_FIXES_END */
"""


def terms_to_html(text):
    parts = []
    for paragraph in text.strip().split("\n\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        parts.append(f"<p>{html.escape(paragraph).replace(chr(10), '<br>')}</p>")
    return "\n".join(parts)


def login(session):
    session.get(urljoin(BASE, "/wp-login.php"), timeout=25)
    resp = session.post(
        urljoin(BASE, "/wp-login.php"),
        data={
            "log": USER,
            "pwd": PASS,
            "wp-submit": "Log In",
            "redirect_to": urljoin(BASE, "/wp-admin/"),
            "testcookie": "1",
        },
        timeout=30,
        allow_redirects=True,
    )
    if "wp-admin" not in resp.url and "Escritorio" not in resp.text and "Dashboard" not in resp.text:
        raise RuntimeError("Login failed")


def hidden_value(text, name):
    for tag in re.findall(r"<input[^>]+>", text, re.I):
        if not re.search(rf'name=["\']{re.escape(name)}["\']', tag, re.I):
            continue
        match = re.search(r'value=["\']([^"\']*)', tag, re.I)
        return html.unescape(match.group(1)) if match else ""
    return ""


def extract_rest_nonce(text):
    patterns = [
        r'wpApiSettings\s*=\s*[^;]*"nonce"\s*:\s*"([^"]+)"',
        r'"nonce"\s*:\s*"([a-f0-9]{10,})"',
        r'wp-api-fetch.*?nonce"\s*:\s*"([^"]+)"',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.S | re.I)
        if match:
            return html.unescape(match.group(1))
    return ""


def update_functions(session):
    editor_url = urljoin(BASE, "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy")
    page = session.get(editor_url, timeout=30)
    page.raise_for_status()

    textarea = re.search(r'<textarea[^>]+name=["\']newcontent["\'][^>]*>(.*?)</textarea>', page.text, re.S)
    if not textarea:
        raise RuntimeError("Could not find functions.php editor textarea")

    current = html.unescape(textarea.group(1))
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"functions_before_today_final_fixes_{datetime.now():%Y%m%d_%H%M%S}.php"
    backup.write_text(current, encoding="utf-8")

    pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.S)
    if pattern.search(current):
        updated = pattern.sub(lambda _: FUNCTIONS_BLOCK.strip(), current)
    else:
        updated = current.rstrip() + "\n\n" + FUNCTIONS_BLOCK.strip() + "\n"

    nonce = hidden_value(page.text, "_wpnonce") or hidden_value(page.text, "nonce")
    if not nonce:
        raise RuntimeError("Could not find theme editor nonce")

    resp = session.post(
        urljoin(BASE, "/wp-admin/theme-editor.php"),
        data={
            "nonce": nonce,
            "_wp_http_referer": "/wp-admin/theme-editor.php?file=functions.php&theme=blocksy",
            "newcontent": updated,
            "action": "update",
            "file": "functions.php",
            "theme": "blocksy",
            "docs-list": "",
            "scrollto": "0",
            "submit": "Actualizar archivo",
        },
        timeout=45,
        allow_redirects=True,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"functions.php update failed: {resp.status_code}")
    return str(backup)


def update_terms_page(session):
    edit_url = urljoin(BASE, f"/wp-admin/post.php?post={TERMS_PAGE_ID}&action=edit")
    edit_page = session.get(edit_url, timeout=35)
    edit_page.raise_for_status()
    nonce = extract_rest_nonce(edit_page.text)
    if not nonce:
        raise RuntimeError("Could not find REST nonce for terms page")

    current_resp = session.get(
        urljoin(BASE, f"/wp-json/wp/v2/pages/{TERMS_PAGE_ID}?context=edit"),
        headers={"X-WP-Nonce": nonce},
        timeout=35,
    )
    current_resp.raise_for_status()
    current = current_resp.json()
    Path("wp-backups").mkdir(exist_ok=True)
    backup = Path("wp-backups") / f"terms_page_751_before_update_{datetime.now():%Y%m%d_%H%M%S}.json"
    backup.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8")

    resp = session.post(
        urljoin(BASE, f"/wp-json/wp/v2/pages/{TERMS_PAGE_ID}"),
        headers={"X-WP-Nonce": nonce, "Content-Type": "application/json"},
        data=json.dumps({"content": terms_to_html(TERMS_TEXT), "status": "publish"}),
        timeout=45,
    )
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"terms page update failed: {resp.status_code} {resp.text[:300]}")
    return str(backup)


def purge_cache(session):
    dashboard = session.get(urljoin(BASE, "/wp-admin/"), timeout=30)
    for href in re.findall(r'href=["\']([^"\']+)["\']', dashboard.text):
        raw = html.unescape(href)
        if "litespeed" in raw.lower() and "purge" in raw.lower():
            session.get(urljoin(BASE, raw), timeout=25)
            return True
    return False


def main():
    session = requests.Session()
    session.headers.update({"User-Agent": "PrimeDropTodayFinalFixes/1.0"})
    login(session)
    functions_backup = update_functions(session)
    terms_backup = update_terms_page(session)
    purged = purge_cache(session)
    print(json.dumps({
        "updated": True,
        "functions_backup": functions_backup,
        "terms_backup": terms_backup,
        "purged": purged,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
