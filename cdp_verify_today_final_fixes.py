import asyncio
import json
import sys
import time
import urllib.parse

import requests
import websockets

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CDP = "http://127.0.0.1:9224"


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


async def open_page(url, width=1200, height=900, mobile=False):
    ws = await websockets.connect(target(url), max_size=20_000_000)
    await call(ws, "Page.enable")
    await call(ws, "Runtime.enable")
    await call(ws, "Emulation.setDeviceMetricsOverride", {
        "width": width,
        "height": height,
        "deviceScaleFactor": 1,
        "mobile": mobile,
        "hasTouch": mobile,
    })
    await call(ws, "Page.navigate", {"url": url})
    await asyncio.sleep(4)
    return ws


async def main():
    ts = str(int(time.time()))
    results = {}

    ws = await open_page("https://primedropelite.com/?verifyfinalday=" + ts)
    results["menu"] = (await call(ws, "Runtime.evaluate", {"expression": r"""
      (() => {
        const links = Array.from(document.querySelectorAll('.pd-bolsos-menu-parent > .pd-bolsos-submenu a')).map(a => ({
          text: a.textContent.trim(),
          href: a.href
        }));
        return {
          links,
          hasHombreMujer: links.some(l => /HOMBRE|MUJER/i.test(l.text)),
          expected: ['TODOS LOS BOLSOS','KARL LAGERFELD','MICHAEL KORS','STEVE MADDEN','TOMMY HILFIGER'].every(t => links.some(l => l.text === t))
        };
      })()
    """, "returnByValue": True}))["result"]["value"]
    await ws.close()

    ws = await open_page("https://primedropelite.com/bolsos/?verifyfinalday=" + ts)
    results["orderby"] = (await call(ws, "Runtime.evaluate", {"expression": r"""
      (() => {
        const select = document.querySelector('select.orderby');
        const option = select && select.querySelector('option');
        const ss = select && getComputedStyle(select);
        const os = option && getComputedStyle(option);
        const filterLinks = Array.from(document.querySelectorAll('.pd-brand-filter a')).map(a => a.textContent.trim());
        return {
          hasSelect: !!select,
          selectColor: ss?.color,
          selectBackground: ss?.backgroundColor,
          optionColor: os?.color,
          optionBackground: os?.backgroundColor,
          filterLinks
        };
      })()
    """, "returnByValue": True}))["result"]["value"]
    await ws.close()

    ws = await open_page("https://primedropelite.com/terminos-y-condiciones/?verifyfinalday=" + ts)
    results["terms"] = (await call(ws, "Runtime.evaluate", {"expression": r"""
      (() => {
        const text = document.body.innerText.replace(/\s+/g, ' ');
        return {
          hasWelcome: text.includes('Welcome to Prime Drop!'),
          hasDisclaimer: text.includes('As long as the website and the information and services on the website are provided free of charge'),
          title: document.querySelector('h1')?.textContent?.trim()
        };
      })()
    """, "returnByValue": True}))["result"]["value"]
    await ws.close()

    ws = await open_page("https://primedropelite.com/product/angel-bag-black/?verifyfinalday=" + ts)
    results["reviews"] = (await call(ws, "Runtime.evaluate", {"expression": r"""
      (() => {
        const review = document.querySelector('.pd-product-reviews-preview');
        const relatedHeading = Array.from(document.querySelectorAll('h2,h3')).find(h => /Productos relacionados/i.test(h.textContent || ''));
        return {
          hasReviewBlock: !!review,
          reviewText: review?.innerText?.replace(/\s+/g, ' ').slice(0, 220),
          relatedHeading: relatedHeading?.textContent?.trim(),
          reviewBeforeRelated: !!(review && relatedHeading && (review.compareDocumentPosition(relatedHeading) & Node.DOCUMENT_POSITION_FOLLOWING))
        };
      })()
    """, "returnByValue": True}))["result"]["value"]
    await ws.close()

    print(json.dumps(results, ensure_ascii=False, indent=2))


asyncio.run(main())
