#!/usr/bin/env python3
"""Pre-renderiza a home: abre _site/index.html num Chromium, espera a pagina montar
e grava o HTML pronto dentro do proprio arquivo. Assim Google e robos de IA leem o texto
sem executar JavaScript. O JavaScript continua rodando por cima (os botoes seguem funcionando).

Requer: pip install playwright && playwright install chromium
"""
import http.server, os, socketserver, sys, threading, functools, re
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, '_site')


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def main():
    handler = functools.partial(Quiet, directory=SITE)
    srv = socketserver.TCPServer(('127.0.0.1', 0), handler)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1280, 'height': 900})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(f'http://127.0.0.1:{port}/', wait_until='networkidle')
        pg.wait_for_selector('#app h1')
        pg.wait_for_timeout(600)
        app = pg.evaluate("document.getElementById('app').innerHTML")
        css = pg.evaluate("document.getElementById('app-css').textContent")
        b.close()
    srv.shutdown()
    if errs:
        sys.exit('Erros de JavaScript na home: ' + '; '.join(errs))
    path = os.path.join(SITE, 'index.html')
    html = open(path, encoding='utf-8').read()
    assert '<div id="app"></div>' in html and '<style id="app-css">/*CSS*/</style>' in html
    html = html.replace('<div id="app"></div>', '<div id="app">' + app + '</div>', 1)
    html = html.replace('<style id="app-css">/*CSS*/</style>', '<style id="app-css">' + css + '</style>', 1)
    open(path, 'w', encoding='utf-8').write(html)
    print(f'pre-render ok: {len(app) // 1024} KB de HTML, h1 presente')


if __name__ == '__main__':
    main()
