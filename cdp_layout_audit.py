import asyncio, base64, json, sys, time, urllib.parse
from pathlib import Path
import requests, websockets

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CDP = "http://127.0.0.1:9224"
OUT = Path("audit-screens")

async def call(ws, method, params=None, _id=[0]):
    _id[0] += 1
    await ws.send(json.dumps({"id": _id[0], "method": method, "params": params or {}}))
    while True:
        data = json.loads(await ws.recv())
        if data.get("id") == _id[0]:
            if "error" in data:
                raise RuntimeError(data["error"])
            return data.get("result", {})

def target(url):
    enc = urllib.parse.quote(url, safe="")
    r = requests.put(f"{CDP}/json/new?{enc}", timeout=10)
    if r.status_code >= 400:
        r = requests.get(f"{CDP}/json/new?{enc}", timeout=10)
    r.raise_for_status()
    return r.json()["webSocketDebuggerUrl"]

async def screenshot(ws, name):
    OUT.mkdir(exist_ok=True)
    img = await call(ws, "Page.captureScreenshot", {"format": "png", "fromSurface": True})
    p = OUT / name
    p.write_bytes(base64.b64decode(img["data"]))
    return str(p.resolve())

async def open_page(url, width, height, mobile):
    ws = await websockets.connect(target(url), max_size=20_000_000)
    await call(ws, "Page.enable")
    await call(ws, "Runtime.enable")
    await call(ws, "Emulation.setDeviceMetricsOverride", {
        "width": width, "height": height, "deviceScaleFactor": 1, "mobile": mobile
    })
    await call(ws, "Page.navigate", {"url": url})
    await asyncio.sleep(4)
    await call(ws, "Runtime.evaluate", {"expression": "document.querySelector('.ct-cookies-accept-button')?.click()", "returnByValue": True})
    await asyncio.sleep(.5)
    return ws

async def main():
    ts = str(int(time.time()))
    results = {}

    # Home mobile: menu + best sellers.
    ws = await open_page("https://primedropelite.com/?nocache=" + ts, 390, 844, True)
    await call(ws, "Runtime.evaluate", {"expression": """
      (() => {
        const h = Array.from(document.querySelectorAll('h1,h2,h3,.elementor-heading-title')).find(el => /VENDIDOS|DESTACADOS/i.test(el.textContent));
        if (h) window.scrollTo(0, h.getBoundingClientRect().top + scrollY - 80);
      })()
    """, "returnByValue": True})
    await asyncio.sleep(1)
    results["home_best_mobile"] = await screenshot(ws, "audit-home-best-mobile-current.png")
    await call(ws, "Runtime.evaluate", {"expression": "window.scrollTo(0,0); document.querySelector('[aria-label=\"Menú\"], .ct-header-trigger')?.click()", "returnByValue": True})
    await asyncio.sleep(1)
    results["menu_mobile"] = await screenshot(ws, "audit-menu-mobile-current.png")
    results["home_mobile_state"] = (await call(ws, "Runtime.evaluate", {"expression": """
      (() => {
        const box = el => { if(!el) return null; const r=el.getBoundingClientRect(); return {x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)} };
        return {
          account: box(document.querySelector('.pd-mobile-account-server')),
          cart: box(Array.from(document.querySelectorAll('a.ct-cart-item,.ct-header-cart')).find(el=>{const r=el.getBoundingClientRect();return r.width>4&&r.height>4;})),
          menu: box(document.querySelector('[aria-label="Menú"], .ct-header-trigger')),
          arrows: Array.from(document.querySelectorAll('.pd-best-arrow')).map(box),
          bestTitle: document.querySelector('.pd-best-title')?.textContent || null
        }
      })()
    """, "returnByValue": True}))["result"]["value"]
    await ws.close()

    # Home tablet header/menu.
    ws = await open_page("https://primedropelite.com/?nocache=" + ts, 768, 1024, True)
    results["tablet_header"] = await screenshot(ws, "audit-tablet-header-current.png")
    results["tablet_state"] = (await call(ws, "Runtime.evaluate", {"expression": """
      (() => {
        const box = el => { if(!el) return null; const r=el.getBoundingClientRect(); return {x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)} };
        return {
          account: box(document.querySelector('.pd-mobile-account-server')),
          cart: box(Array.from(document.querySelectorAll('a.ct-cart-item,.ct-header-cart')).find(el=>{const r=el.getBoundingClientRect();return r.width>4&&r.height>4;})),
          menu: box(document.querySelector('[aria-label="Menú"], .ct-header-trigger'))
        }
      })()
    """, "returnByValue": True}))["result"]["value"]
    await call(ws, "Runtime.evaluate", {"expression": "document.querySelector('[aria-label=\"Menú\"], .ct-header-trigger')?.click()", "returnByValue": True})
    await asyncio.sleep(1)
    results["menu_tablet"] = await screenshot(ws, "audit-menu-tablet-current.png")
    await ws.close()

    # Product page mobile.
    ws = await open_page("https://primedropelite.com/product/cheyann-bag-black/?nocache=" + ts, 390, 844, True)
    results["product_mobile"] = await screenshot(ws, "audit-product-cheyann-mobile-current.png")
    results["product_state"] = (await call(ws, "Runtime.evaluate", {"expression": """
      (() => {
        const sel = '.product, main, .summary, .woocommerce-product-gallery, h1.product_title, .single_add_to_cart_button';
        return Array.from(document.querySelectorAll(sel)).map(el=>{
          const r=el.getBoundingClientRect(); return {tag:el.tagName, cls:el.className, text:(el.textContent||'').trim().replace(/\\s+/g,' ').slice(0,70), x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height)};
        }).filter(x=>x.w>0 && x.h>0);
      })()
    """, "returnByValue": True}))["result"]["value"]
    # Add and checkout.
    await call(ws, "Runtime.evaluate", {"expression": "document.querySelector('button.single_add_to_cart_button, .single_add_to_cart_button')?.click()", "returnByValue": True})
    await asyncio.sleep(2)
    await call(ws, "Page.navigate", {"url": "https://primedropelite.com/checkout/?nocache=" + ts})
    await asyncio.sleep(4)
    results["checkout_mobile"] = await screenshot(ws, "audit-checkout-mobile-current.png")
    results["checkout_state"] = (await call(ws, "Runtime.evaluate", {"expression": """
      (() => {
        const names=['main','.woocommerce-checkout','#customer_details','.woocommerce-billing-fields','.woocommerce-checkout-review-order','form.checkout'];
        return names.map(s=>{
          const el=document.querySelector(s); if(!el) return null; const r=el.getBoundingClientRect();
          return {selector:s, x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height), text:(el.textContent||'').trim().replace(/\\s+/g,' ').slice(0,80)};
        }).filter(Boolean);
      })()
    """, "returnByValue": True}))["result"]["value"]
    await ws.close()

    print(json.dumps(results, ensure_ascii=False, indent=2))

asyncio.run(main())
