import asyncio
import json
import time
import urllib.parse

import requests
import websockets

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


async def main():
    url = "https://primedropelite.com/?mobilemenufix=" + str(int(time.time()))
    ws = await websockets.connect(target(url), max_size=20_000_000)
    await call(ws, "Page.enable")
    await call(ws, "Runtime.enable")
    await call(ws, "Emulation.setDeviceMetricsOverride", {
        "width": 390,
        "height": 844,
        "deviceScaleFactor": 1,
        "mobile": True,
        "hasTouch": True,
    })
    await call(ws, "Page.navigate", {"url": url})
    await asyncio.sleep(4)

    menu_result = (await call(ws, "Runtime.evaluate", {"expression": r"""
      (() => {
        const before = location.href;
        const visible = el => {
          if (!el) return false;
          const r = el.getBoundingClientRect();
          const s = getComputedStyle(el);
          return r.width > 5 && r.height > 5 && s.display !== 'none' && s.visibility !== 'hidden' && s.opacity !== '0';
        };
        const trigger = Array.from(document.querySelectorAll('button,a,[role="button"]')).find(el => {
          const txt = ((el.getAttribute('aria-label') || '') + ' ' + (el.textContent || '')).toLowerCase();
          return visible(el) && (txt.includes('menu') || txt.includes('menú') || el.className.toString().includes('trigger'));
        });
        if (trigger) trigger.click();
        return new Promise(resolve => setTimeout(() => {
          const link = Array.from(document.querySelectorAll('li.pd-bolsos-menu-parent > a')).find(a => /^BOLSOS$/i.test((a.textContent || '').trim()) && visible(a));
          if (!link) return resolve({before, hasTrigger: !!trigger, hasBolsosLink: false, hrefAfterClick: location.href});
          const li = link.closest('li');
          link.click();
          setTimeout(() => {
            const items = Array.from(li.querySelectorAll('.pd-bolsos-submenu a')).filter(visible).map(a => a.textContent.trim());
            resolve({
              before,
              hasTrigger: !!trigger,
              hasBolsosLink: true,
              hrefAfterClick: location.href,
              stayed: location.href === before,
              open: li.classList.contains('pd-submenu-open'),
              items
            });
          }, 500);
        }, 700));
      })()
    """, "awaitPromise": True, "returnByValue": True}))["result"]["value"]

    cart_result = (await call(ws, "Runtime.evaluate", {"expression": r"""
      (() => {
        const visible = el => {
          if (!el) return false;
          const r = el.getBoundingClientRect();
          const s = getComputedStyle(el);
          return r.width > 5 && r.height > 5 && s.display !== 'none' && s.visibility !== 'hidden' && s.opacity !== '0';
        };
        const cart = Array.from(document.querySelectorAll('header a[href*="cart"], header .ct-header-cart a, header .ct-cart-item, header [data-id="cart"] a')).find(visible);
        if (cart) cart.click();
        return new Promise(resolve => setTimeout(() => {
          const title = Array.from(document.querySelectorAll('.pd-cart-drawer-header h3,.cart-drawer-header h3,#cart-drawer h3,.pd-cart-drawer h3,.cart-drawer h3')).find(visible);
          resolve({
            hasCartTarget: !!cart,
            title: title ? title.textContent.trim() : null,
            url: location.href
          });
        }, 1200));
      })()
    """, "awaitPromise": True, "returnByValue": True}))["result"]["value"]

    print(json.dumps({"menu": menu_result, "cart": cart_result}, ensure_ascii=False, indent=2))
    await ws.close()


asyncio.run(main())
