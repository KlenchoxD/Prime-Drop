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

async def open_page(url, width=1365, height=768, mobile=False):
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

async def screenshot(ws, name):
    OUT.mkdir(exist_ok=True)
    img = await call(ws, "Page.captureScreenshot", {"format": "png", "fromSurface": True})
    p = OUT / name
    p.write_bytes(base64.b64decode(img["data"]))
    return str(p.resolve())

async def inspect(ws):
    expression = r"""
    (() => {
      const box = el => {
        if (!el) return null;
        const r = el.getBoundingClientRect();
        return {x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height)};
      };
      const firstProducts = Array.from(document.querySelectorAll('.woocommerce ul.products li.product')).slice(0,3).map(el => {
        const img = el.querySelector('img');
        const title = el.querySelector('.woocommerce-loop-product__title');
        const btn = el.querySelector('.button');
        return {card:box(el), img:box(img), title:box(title), btn:box(btn), text:(title?.textContent||'').trim()};
      });
      return {
        header: box(document.querySelector('#header, header, .ct-header')),
        title: box(document.querySelector('h1, .page-title')),
        shopControls: box(document.querySelector('.woocommerce-result-count')?.parentElement || document.querySelector('.woocommerce-ordering')?.parentElement),
        resultCount: box(document.querySelector('.woocommerce-result-count')),
        search: box(document.querySelector('.pd-shop-search, form[role="search"]')),
        orderby: box(document.querySelector('.woocommerce-ordering')),
        sidebar: box(document.querySelector('aside, .ct-sidebar, .shop-sidebar')),
        grid: box(document.querySelector('.woocommerce ul.products')),
        firstProducts,
        bodyText: document.body.innerText.replace(/\s+/g,' ').slice(0,220)
      };
    })()
    """
    return (await call(ws, "Runtime.evaluate", {"expression": expression, "returnByValue": True}))["result"]["value"]

async def main():
    ts = str(int(time.time()))
    results = {}
    ws = await open_page("https://primedropelite.com/bolsos/?nocache=" + ts)
    results["prime_desktop_png"] = await screenshot(ws, "audit-prime-bolsos-desktop-current.png")
    results["prime_desktop_state"] = await inspect(ws)
    await ws.close()

    ws = await open_page("https://luxiumstore.com/collections/hombres?nocache=" + ts)
    results["luxium_desktop_png"] = await screenshot(ws, "audit-luxium-hombres-desktop-reference.png")
    results["luxium_desktop_state"] = await inspect(ws)
    await ws.close()

    ws = await open_page("https://primedropelite.com/bolsos/?nocache=" + ts, 390, 844, True)
    results["prime_mobile_png"] = await screenshot(ws, "audit-prime-bolsos-mobile-current.png")
    results["prime_mobile_state"] = await inspect(ws)
    await ws.close()

    ws = await open_page("https://primedropelite.com/bolsos/?nocache=" + ts, 768, 1024, True)
    results["prime_tablet_png"] = await screenshot(ws, "audit-prime-bolsos-tablet-current.png")
    results["prime_tablet_state"] = await inspect(ws)
    await ws.close()

    print(json.dumps(results, ensure_ascii=False, indent=2))

asyncio.run(main())
