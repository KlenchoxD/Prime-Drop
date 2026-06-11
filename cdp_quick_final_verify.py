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

async def shot(ws, name):
    OUT.mkdir(exist_ok=True)
    img = await call(ws, "Page.captureScreenshot", {"format": "png", "fromSurface": True})
    p = OUT / name
    p.write_bytes(base64.b64decode(img["data"]))
    return str(p.resolve())

async def page(url, width=900, height=760, mobile=False):
    ws = await websockets.connect(target(url), max_size=20_000_000)
    await call(ws, "Page.enable")
    await call(ws, "Runtime.enable")
    await call(ws, "Emulation.setDeviceMetricsOverride", {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": mobile})
    await call(ws, "Page.navigate", {"url": url})
    await asyncio.sleep(4)
    return ws

async def main():
    ts = str(int(time.time()))
    results = {}

    ws = await page("https://primedropelite.com/wishlist/?finalverify=" + ts, 1366, 760, False)
    results["wishlist_shot"] = await shot(ws, "audit-wishlist-final.png")
    results["wishlist_state"] = (await call(ws, "Runtime.evaluate", {"expression": """
      (() => {
        const clean = document.querySelector('.pd-wishlist-empty-clean');
        const table = document.querySelector('.wishlist_table');
        const empty = document.querySelector('.wishlist-empty');
        return {
          hasClean: !!clean,
          hasTable: !!table,
          hasEmpty: !!empty,
          bodyClasses: document.body.className,
          headingTexts: Array.from(document.querySelectorAll('h1,h2,h3')).map(h=>h.textContent.trim()).slice(0,8),
          visibleText: document.body.innerText.replace(/\\s+/g,' ').slice(0,400)
        };
      })()
    """, "returnByValue": True}))["result"]["value"]
    await ws.close()

    ws = await page("https://primedropelite.com/product/angel-bag-black/?finalverify=" + ts, 390, 844, True)
    await call(ws, "Runtime.evaluate", {"expression": "document.querySelector('button.single_add_to_cart_button, .single_add_to_cart_button')?.click()", "returnByValue": True})
    await asyncio.sleep(1.5)
    await call(ws, "Page.navigate", {"url": "https://primedropelite.com/checkout/?finalverify=" + ts})
    await asyncio.sleep(5)
    results["checkout_top_shot"] = await shot(ws, "audit-checkout-top-final.png")
    results["checkout_state"] = (await call(ws, "Runtime.evaluate", {"expression": """
      (() => {
        const login = document.querySelector('.woocommerce-form-login-toggle .woocommerce-info');
        const drawer = document.querySelector('#cart-drawer, .cart-drawer, .pd-cart-drawer');
        const payTitle = document.querySelector('#payment .pd-payment-title');
        const style = login ? getComputedStyle(login) : null;
        return {
          loginText: login?.innerText.replace(/\\s+/g,' '),
          loginRect: login ? Object.fromEntries(['x','y','width','height'].map(k=>[k,Math.round(login.getBoundingClientRect()[k])])) : null,
          loginDisplay: style?.display,
          beforeDisplay: login ? getComputedStyle(login, '::before').display : null,
          drawerVisible: drawer ? getComputedStyle(drawer).display + ' / ' + getComputedStyle(drawer).visibility : null,
          payTitle: payTitle?.textContent?.trim(),
          bodyPosition: getComputedStyle(document.body).position,
          visibleText: document.body.innerText.replace(/\\s+/g,' ').slice(0,500)
        };
      })()
    """, "returnByValue": True}))["result"]["value"]
    await ws.close()

    print(json.dumps(results, ensure_ascii=False, indent=2))

asyncio.run(main())
