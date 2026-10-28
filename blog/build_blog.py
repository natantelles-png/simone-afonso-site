#!/usr/bin/env python3
"""Gera o site estatico final em _site/ a partir do index.html e dos posts do Supabase.

Uso:
  SUPABASE_URL=... SUPABASE_ANON_KEY=... python3 blog/build_blog.py
  python3 blog/build_blog.py --fixture blog/fixture/posts.json     (teste local, sem rede)

Cada post vira uma pagina fixa (HTML puro, sem JavaScript) com:
titulo e meta, canonical, Open Graph, JSON-LD (BlogPosting, BreadcrumbList, FAQPage,
Person e ProfessionalService), resposta rapida, sumario, FAQ visivel e caixa da autora.
Tambem gera indice do blog, categorias, paginacao, sitemap.xml, feed.xml, robots.txt,
llms.txt e posts.json (usado pela home).
"""
import argparse, datetime as dt, hashlib, html, json, os, re, shutil, sys, unicodedata, urllib.request, urllib.parse
from html.parser import HTMLParser
from email.utils import format_datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '_site')
CFG = json.load(open(os.path.join(ROOT, 'blog', 'config.json'), encoding='utf-8'))
SITE = CFG['site_url'].rstrip('/')
PER_PAGE = 12
MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
esc = html.escape


# ---------------------------------------------------------------- utilidades
def slugify(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def parse_dt(v):
    if not v:
        return dt.datetime.now(dt.timezone.utc)
    d = dt.datetime.fromisoformat(str(v).replace('Z', '+00:00'))
    return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)


def br_date(d):
    d = d.astimezone(dt.timezone(dt.timedelta(hours=-3)))
    return f'{d.day} de {MESES[d.month - 1]} de {d.year}'


def iso(d):
    return d.astimezone(dt.timezone(dt.timedelta(hours=-3))).isoformat(timespec='seconds')


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>'


def plain(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s or ''))).strip()


def trunc(s, n):
    s = plain(s)
    return s if len(s) <= n else s[:n - 1].rsplit(' ', 1)[0].rstrip(' ,;:.') + '…'


def write(path, content, binary=False):
    p = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'wb' if binary else 'w', **({} if binary else {'encoding': 'utf-8'})).write(content)


# ---------------------------------------------------------------- sanitizacao
ALLOWED = {'p', 'h2', 'h3', 'h4', 'strong', 'em', 'ul', 'ol', 'li', 'blockquote', 'a', 'img', 'br', 'hr', 'figure', 'figcaption'}
RENAME = {'b': 'strong', 'i': 'em', 'h1': 'h2', 'h5': 'h4', 'h6': 'h4', 'div': 'p'}
DROP_WITH_CONTENT = {'script', 'style', 'iframe', 'object', 'embed', 'form', 'noscript', 'template', 'svg', 'math'}
VOID = {'br', 'hr', 'img'}
BLOCKS = {'ul', 'ol', 'h2', 'h3', 'h4', 'blockquote', 'figure', 'hr'}
SAFE_HREF = re.compile(r'^(https?://|mailto:|tel:|/|#)', re.I)
SAFE_SRC = re.compile(r'^(https://|/|[A-Za-z0-9_./-]+$)', re.I)


class Clean(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.stack, self.skip = [], [], 0

    def handle_starttag(self, tag, attrs):
        tag = RENAME.get(tag, tag)
        if tag in DROP_WITH_CONTENT:
            self.skip += 1
            return
        if self.skip or tag not in ALLOWED:
            return
        a = dict(attrs)
        if tag in BLOCKS and self.stack and self.stack[-1] == 'p':
            self.stack.pop()
            self.out.append('</p>')
        if tag == 'p' and self.stack and self.stack[-1] in ('p', 'li', 'blockquote', 'h2', 'h3', 'h4'):
            return  # <div> dentro de bloco: ignora
        if tag == 'a':
            href = (a.get('href') or '').strip()
            if not SAFE_HREF.match(href):
                return
            ext = href.lower().startswith('http') and SITE.split('//')[1] not in href
            self.out.append(f'<a href="{esc(href, True)}"' + (' rel="noopener" target="_blank"' if ext else '') + '>')
        elif tag == 'img':
            src = (a.get('src') or '').strip()
            if not SAFE_SRC.match(src):
                return
            self.out.append(f'<img src="{esc(src, True)}" alt="{esc((a.get("alt") or "").strip(), True)}" loading="lazy" decoding="async">')
            return
        elif tag in VOID:
            self.out.append(f'<{tag}>')
            return
        else:
            self.out.append(f'<{tag}>')
        self.stack.append(tag)

    def handle_endtag(self, tag):
        tag = RENAME.get(tag, tag)
        if tag in DROP_WITH_CONTENT:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip or tag not in ALLOWED or tag in VOID:
            return
        if tag == 'p' and (not self.stack or self.stack[-1] != 'p'):
            return
        if tag in self.stack:
            while self.stack:
                t = self.stack.pop()
                self.out.append(f'</{t}>')
                if t == tag:
                    break

    def handle_data(self, data):
        if not self.skip:
            self.out.append(esc(data, quote=False))

    def result(self):
        while self.stack:
            self.out.append(f'</{self.stack.pop()}>')
        return ''.join(self.out)


def sanitize(raw):
    c = Clean()
    c.feed(raw or '')
    c.close()
    h = c.result()
    # texto solto no topo vira paragrafo; remove paragrafos vazios
    h = re.sub(r'<p>(\s|&nbsp;|<br>)*</p>', '', h)
    h = re.sub(r'(<(?:li|p|h[234]|blockquote)>)\s*(?:<br>)+', r'\1', h)
    return h.strip()


def add_heading_ids(h):
    seen, toc = {}, []

    def rep(m):
        lvl, inner = m.group(1), m.group(2)
        base = slugify(plain(inner)) or 'secao'
        n = seen.get(base, 0)
        seen[base] = n + 1
        hid = base if n == 0 else f'{base}-{n + 1}'
        if lvl == '2':
            toc.append((hid, plain(inner)))
        return f'<h{lvl} id="{hid}">{inner}</h{lvl}>'

    return re.sub(r'<h([23])>(.*?)</h\1>', rep, h, flags=re.S), toc


# ---------------------------------------------------------------- imagens
IMG_CACHE = {}


def localize_image(url, fixture_dir):
    """Baixa a imagem para o proprio dominio (mais rapido e independente). Devolve (caminho, largura, altura)."""
    if not url:
        return None
    if url in IMG_CACHE:
        return IMG_CACHE[url]
    ext = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower() or '.jpg'
    if ext not in ('.jpg', '.jpeg', '.png', '.webp'):
        ext = '.jpg'
    name = hashlib.sha1(url.encode()).hexdigest()[:12] + ext
    dest = os.path.join(OUT, 'blog', 'img', name)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        if url.startswith('http'):
            req = urllib.request.Request(url, headers={'User-Agent': 'sa-site-build'})
            with urllib.request.urlopen(req, timeout=40) as r:
                open(dest, 'wb').write(r.read())
        elif fixture_dir and os.path.exists(os.path.join(fixture_dir, url)):
            shutil.copy(os.path.join(fixture_dir, url), dest)
        else:
            return None
    except Exception as e:
        print('  aviso: imagem nao baixada', url, e, file=sys.stderr)
        return None
    w = h = None
    try:
        from PIL import Image
        w, h = Image.open(dest).size
    except Exception:
        pass
    IMG_CACHE[url] = (f'/blog/img/{name}', w, h)
    return IMG_CACHE[url]


def localize_body_images(h, fixture_dir):
    def rep(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag).group(1)
        loc = localize_image(html.unescape(src), fixture_dir)
        if not loc:
            return tag
        path, w, hh = loc
        tag = tag.replace(f'src="{src}"', f'src="{path}"' + (f' width="{w}" height="{hh}"' if w else ''))
        return tag

    return re.sub(r'<img [^>]+>', rep, h)


# ---------------------------------------------------------------- entidades (JSON-LD)
def entities():
    person = {
        '@type': 'Person', '@id': SITE + '/#simone', 'name': CFG['author'], 'jobTitle': CFG['author_role'],
        'url': SITE + '/', 'image': SITE + '/blog/assets/simone.jpg', 'sameAs': [CFG['instagram']],
        'knowsAbout': CFG['knows_about'], 'worksFor': {'@id': SITE + '/#negocio'},
    }
    biz = {
        '@type': ['ProfessionalService', 'LocalBusiness'], '@id': SITE + '/#negocio', 'name': CFG['name'], 'url': SITE + '/',
        'logo': SITE + '/blog/assets/logo-ameixa.png', 'image': SITE + '/og.jpg', 'telephone': CFG['phone'],
        'description': CFG['description'], 'founder': {'@id': SITE + '/#simone'}, 'sameAs': [CFG['instagram']],
        'areaServed': [{'@type': 'AdministrativeArea', 'name': 'Espírito Santo'}, {'@type': 'City', 'name': 'Vitória'}],
        'address': {'@type': 'PostalAddress', 'addressLocality': CFG['locality'], 'addressRegion': CFG['region'], 'addressCountry': 'BR'},
        'knowsAbout': CFG['knows_about'], 'priceRange': '$$',
    }
    site = {'@type': 'WebSite', '@id': SITE + '/#site', 'url': SITE + '/', 'name': CFG['name'], 'inLanguage': 'pt-BR', 'publisher': {'@id': SITE + '/#negocio'}}
    return person, biz, site


# ---------------------------------------------------------------- layout
def head(title, desc, path, og_image=None, og_type='website', extra='', robots='index,follow,max-image-preview:large,max-snippet:-1'):
    url = SITE + path
    img = og_image or SITE + '/og.jpg'
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc, True)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="alternate" type="application/rss+xml" title="{esc(CFG['name'], True)}" href="{SITE}/blog/feed.xml">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="{esc(CFG['name'], True)}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title, True)}">
<meta property="og:description" content="{esc(desc, True)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title, True)}">
<meta name="twitter:description" content="{esc(desc, True)}">
<meta name="twitter:image" content="{img}">
<meta name="theme-color" content="#534243">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gloock&display=swap">
<link rel="stylesheet" href="/blog/assets/blog.css?v={CSS_V}">
{extra}
</head>
<body>
<a class="pular" href="#conteudo">Pular para o conteúdo</a>
<header class="topo"><div class="wrap">
<a href="/" aria-label="Simone Afonso, página inicial"><img src="/blog/assets/logo-ameixa.png" alt="Simone Afonso" width="92" height="53"></a>
<nav class="menu" aria-label="Principal"><a href="/">Início</a><a href="/#projetos">Projetos</a><a class="fica" href="/blog/">Blog</a><a class="zap" href="{wa('Olá, Simone! Vim pelo blog e gostaria de conversar sobre um projeto.')}">Falar no WhatsApp</a></nav>
</div></header>
<main id="conteudo">
'''


def foot():
    ig = CFG['instagram']
    return f'''</main>
<footer class="rodape"><div class="wrap">
<div class="cols">
<div><img src="/blog/assets/logo-branco.png" alt="Simone Afonso" width="110" height="63" loading="lazy">
<p>{esc(CFG['author_role'])}</p></div>
<div><p><strong>Atendimento</strong></p><p>Online e a domicílio, na Grande Vitória e em todo o ES</p></div>
<div><p><strong>Contato</strong></p><p><a href="{wa('Olá, Simone!')}">WhatsApp {esc(CFG['phone'])}</a></p><p><a href="{ig}" rel="noopener">@simoneafonso.arq</a></p></div>
<div><p><strong>Site</strong></p><p><a href="/">Início</a></p><p><a href="/blog/">Blog</a></p><p><a href="/blog/feed.xml">Feed RSS</a></p></div>
</div>
<small>© {dt.date.today().year} Simone Afonso. Todos os direitos reservados.</small>
</div></footer>
</body>
</html>
'''


def wa(msg):
    return f"https://wa.me/{CFG['whatsapp']}?text=" + urllib.parse.quote(msg)


def card(p, lazy=True):
    img = f'<img src="{p["cover"]}" alt="{esc(p["cover_alt"], True)}" {p["dims"]}{" loading=lazy decoding=async" if lazy else ""}>' if p['cover'] else ''
    return f'''<li><article class="card">{img}<div class="info">
<span class="kicker">{esc(p['category'])}</span>
<h3><a href="{p['path']}">{esc(p['title'])}</a></h3>
<p>{esc(trunc(p['excerpt'] or p['answer'], 140))}</p>
<time datetime="{iso(p['published'])}">{br_date(p['published'])}</time></div></article></li>'''


# ---------------------------------------------------------------- paginas
def post_page(p, posts):
    person, biz, site = entities()
    url = SITE + p['path']
    crumbs = [('Início', SITE + '/'), ('Blog', SITE + '/blog/'), (p['category'], SITE + p['cat_path']), (p['title'], url)]
    ld_post = {
        '@type': 'BlogPosting', '@id': url + '#post', 'mainEntityOfPage': {'@type': 'WebPage', '@id': url},
        'headline': trunc(p['title'], 110), 'description': trunc(p['excerpt'] or p['answer'], 300), 'inLanguage': 'pt-BR',
        'datePublished': iso(p['published']), 'dateModified': iso(p['modified']), 'articleSection': p['category'],
        'wordCount': p['words'], 'author': {'@id': SITE + '/#simone'}, 'publisher': {'@id': SITE + '/#negocio'},
        'isPartOf': {'@id': SITE + '/#site'},
        'speakable': {'@type': 'SpeakableSpecification', 'cssSelector': ['h1', '.resposta p']},
    }
    if p['cover']:
        ld_post['image'] = [SITE + p['cover']]
    if p['keywords']:
        ld_post['keywords'] = p['keywords']
    graph = [person, biz, site, ld_post, {
        '@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(crumbs)]}]
    if p['faq']:
        graph.append({'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [
            {'@type': 'Question', 'name': q['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': q['a']}} for q in p['faq']]})
    title = p['title'] if len(p['title']) > 48 else f"{p['title']} | Simone Afonso"
    og_img = SITE + p['cover'] if p['cover'] else None
    extra = jsonld({'@context': 'https://schema.org', '@graph': graph}) + f'''
<meta property="article:published_time" content="{iso(p['published'])}">
<meta property="article:modified_time" content="{iso(p['modified'])}">
<meta property="article:section" content="{esc(p['category'], True)}">
<meta property="article:author" content="{esc(CFG['author'], True)}">'''
    h = head(title, trunc(p['excerpt'] or p['answer'], 160), p['path'], og_img, 'article', extra)
    atual = ''
    if (p['modified'] - p['published']).days >= 1:
        atual = f' · Atualizado em <time datetime="{iso(p["modified"])}">{br_date(p["modified"])}</time>'
    toc = ''
    if len(p['toc']) >= 3:
        toc = '<nav class="sumario" aria-label="Neste texto"><b>Neste texto</b><ol>' + ''.join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in p['toc']) + '</ol></nav>'
    cover = ''
    if p['cover']:
        cover = f'<figure class="capa"><img src="{p["cover"]}" alt="{esc(p["cover_alt"], True)}" {p["dims"]} fetchpriority="high" decoding="async"></figure>'
    resposta = f'<aside class="resposta" aria-label="Resposta rápida"><span class="rotulo">Resposta rápida</span><p>{esc(p["answer"])}</p></aside>' if p['answer'] else ''
    faq = ''
    if p['faq']:
        faq = '<section class="faq" aria-labelledby="faq-t"><h2 id="faq-t">Perguntas frequentes</h2><dl>' + ''.join(
            f'<dt>{esc(q["q"])}</dt><dd><p>{esc(q["a"])}</p></dd>' for q in p['faq']) + '</dl></section>'
    rel = [x for x in posts if x['slug'] != p['slug']]
    rel.sort(key=lambda x: (x['category'] != p['category'], -x['published'].timestamp()))
    relhtml = ''
    if rel:
        relhtml = '<section class="relacionados wrap" aria-labelledby="rel-t"><h2 id="rel-t">Continue lendo</h2><ul class="grade">' + ''.join(card(x) for x in rel[:3]) + '</ul></section>'
    cau = f'<p>{esc(CFG["credentials"])}</p>' if CFG.get('credentials') else ''
    body = f'''<div class="narrow">
<nav class="trilha" aria-label="Você está em"><ol>{''.join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in crumbs[:3])}<li aria-current="page">{esc(trunc(p['title'], 48))}</li></ol></nav>
<article>
<header><span class="kicker"><a href="{p['cat_path']}">{esc(p['category'])}</a></span>
<h1>{esc(p['title'])}</h1>
<div class="byline"><img src="/blog/assets/simone.jpg" alt="Simone Afonso" width="52" height="52"><div>Por <strong>{esc(CFG['author'])}</strong>, {esc(CFG['author_role'].lower())}<br>
Publicado em <time datetime="{iso(p['published'])}">{br_date(p['published'])}</time>{atual} · {p['minutes']} min de leitura</div></div></header>
{resposta}
{cover}
{toc}
<div class="corpo">{p['body']}</div>
{faq}
<aside class="autora" aria-label="Sobre a autora"><img src="/blog/assets/simone.jpg" alt="Simone Afonso" width="84" height="84" loading="lazy">
<div><h2>{esc(CFG['author'])}</h2><p>{esc(CFG['bio'])}</p>{cau}<p><a href="/">Conheça o trabalho da Simone</a> · <a href="{CFG['instagram']}" rel="noopener">Instagram</a></p></div></aside>
<section class="cta" aria-labelledby="cta-t"><h2 id="cta-t">Quer aplicar isso no seu espaço?</h2>
<p>Conte para a Simone o que você precisa. A conversa é online ou na sua casa, sem compromisso.</p>
<a class="botao" href="{wa('Olá, Simone! Li o texto “' + p['title'] + '” e gostaria de conversar sobre um projeto.')}">Chamar no WhatsApp</a></section>
</article></div>
{relhtml}
'''
    return h + body + foot()


def list_page(title, desc, path, heading, lead, posts, cats, active, page, pages, base):
    person, biz, site = entities()
    items = [{'@type': 'ListItem', 'position': i + 1, 'url': SITE + p['path'], 'name': p['title']} for i, p in enumerate(posts)]
    crumbs = [('Início', SITE + '/'), ('Blog', SITE + '/blog/')] + ([(active, SITE + path)] if active else [])
    graph = [person, biz, site,
             {'@type': 'CollectionPage', '@id': SITE + path + '#pagina', 'url': SITE + path, 'name': title, 'description': desc, 'inLanguage': 'pt-BR', 'isPartOf': {'@id': SITE + '/#site'}},
             {'@type': 'ItemList', 'itemListElement': items},
             {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(crumbs)]}]
    extra = jsonld({'@context': 'https://schema.org', '@graph': graph})
    if page > 1:
        extra += f'\n<link rel="prev" href="{SITE}{base if page == 2 else base + "pagina/" + str(page - 1) + "/"}">'
    if page < pages:
        extra += f'\n<link rel="next" href="{SITE}{base}pagina/{page + 1}/">'
    h = head(title, desc, path, None, 'website', extra)
    chips = f'<li><a href="/blog/"{" aria-current=page" if not active else ""}>Todos</a></li>' + ''.join(
        f'<li><a href="/blog/{slugify(c)}/"{" aria-current=page" if c == active else ""}>{esc(c)}</a></li>' for c in cats)
    pag = ''
    if pages > 1:
        links = []
        for n in range(1, pages + 1):
            href = base if n == 1 else f'{base}pagina/{n}/'
            links.append(f'<span aria-current="page">{n}</span>' if n == page else f'<a href="{href}">{n}</a>')
        pag = '<nav class="paginas" aria-label="Páginas">' + ''.join(links) + '</nav>'
    grid = ('<ul class="grade">' + ''.join(card(p, i > 1) for i, p in enumerate(posts)) + '</ul>') if posts else '<p class="vazio">Os primeiros textos chegam em breve.</p>'
    return h + f'''<div class="wrap">
<nav class="trilha" aria-label="Você está em"><ol>{''.join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in crumbs[:-1])}<li aria-current="page">{esc(crumbs[-1][0])}</li></ol></nav>
<div class="cabeca"><span class="kicker">Blog</span><h1>{esc(heading)}</h1><p class="lead">{esc(lead)}</p>
<ul class="filtros" aria-label="Filtrar por assunto">{chips}</ul></div>
{grid}{pag}
</div>
''' + foot()


# ---------------------------------------------------------------- principal
def load_posts(args):
    if args.fixture:
        d = json.load(open(args.fixture, encoding='utf-8'))
        return d, os.path.dirname(os.path.abspath(args.fixture))
    url, key = os.environ.get('SUPABASE_URL', '').rstrip('/'), os.environ.get('SUPABASE_ANON_KEY', '')
    if not url or not key:
        sys.exit('Defina SUPABASE_URL e SUPABASE_ANON_KEY (ou use --fixture).')
    now = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    q = f'{url}/rest/v1/posts?select=*&status=eq.published&publish_at=lte.{now}&order=publish_at.desc'
    req = urllib.request.Request(q, headers={'apikey': key, 'Authorization': 'Bearer ' + key})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read()), None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fixture')
    args = ap.parse_args()
    global CSS_V
    CSS_V = hashlib.md5(open(os.path.join(ROOT, 'blog', 'static', 'blog.css'), 'rb').read()).hexdigest()[:8]

    raw, fdir = load_posts(args)
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    # arquivos estaticos do site
    home = os.path.join(ROOT, '_home')
    if not os.path.exists(os.path.join(home, 'index.html')):
        sys.exit('Falta _home/. Rode antes: python3 build/build.py')
    shutil.copytree(home, OUT, dirs_exist_ok=True)
    for f in ('CNAME', '404.html', 'favicon.png', 'og.jpg'):
        if os.path.exists(os.path.join(ROOT, f)):
            shutil.copy(os.path.join(ROOT, f), os.path.join(OUT, f))
    shutil.copytree(os.path.join(ROOT, 'blog', 'static'), os.path.join(OUT, 'blog', 'assets'))
    open(os.path.join(OUT, '.nojekyll'), 'a').close()

    posts, seen = [], {'assets', 'img', 'pagina', 'feed', 'posts'}
    seen |= {slugify((r.get('category') or '').strip()) for r in raw}
    for r in raw:
        slug = r.get('slug', '')
        if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', slug) or slug in seen or not r.get('title'):
            print('  aviso: post ignorado (slug ou titulo invalido):', slug, file=sys.stderr)
            continue
        seen.add(slug)
        body = sanitize(r.get('body_html'))
        body = localize_body_images(body, fdir)
        body, toc = add_heading_ids(body)
        cover = localize_image((r.get('cover_url') or '').strip(), fdir)
        faq = [{'q': plain(x.get('q')), 'a': plain(x.get('a'))} for x in (r.get('faq') or []) if plain(x.get('q')) and plain(x.get('a'))]
        words = len(plain(body).split())
        cat = (r.get('category') or 'Blog').strip()
        posts.append({
            'slug': slug, 'path': f'/blog/{slug}/', 'title': plain(r['title']), 'category': cat, 'cat_path': f'/blog/{slugify(cat)}/',
            'excerpt': plain(r.get('excerpt')), 'answer': plain(r.get('answer')), 'keywords': plain(r.get('keywords')),
            'body': body, 'toc': toc, 'faq': faq, 'words': words, 'minutes': max(1, round(words / 200)),
            'cover': cover[0] if cover else None, 'cover_alt': plain(r.get('cover_alt')) or plain(r['title']),
            'dims': f'width="{cover[1]}" height="{cover[2]}"' if cover and cover[1] else '',
            'published': parse_dt(r.get('publish_at')), 'modified': parse_dt(r.get('updated_at') or r.get('publish_at')),
        })
    posts.sort(key=lambda p: p['published'], reverse=True)
    cats = []
    for p in posts:
        if p['category'] not in cats:
            cats.append(p['category'])

    for p in posts:
        write(f"blog/{p['slug']}/index.html", post_page(p, posts))

    def paginate(lst, base, title, desc, heading, lead, active):
        pages = max(1, -(-len(lst) // PER_PAGE))
        for n in range(1, pages + 1):
            chunk = lst[(n - 1) * PER_PAGE:n * PER_PAGE]
            path = base if n == 1 else f'{base}pagina/{n}/'
            t = title if n == 1 else f'{title} (página {n})'
            write(path.lstrip('/') + 'index.html', list_page(t, desc, path, heading, lead, chunk, cats, active, n, pages, base))

    paginate(posts, '/blog/', 'Blog de Simone Afonso: neuroarquitetura e arquitetura de interiores',
             'Textos da arquiteta Simone Afonso sobre neuroarquitetura, projetos comerciais, Home Relooking e Home Staging, com orientações práticas para casas e empresas no Espírito Santo.',
             'Caderno da Simone', 'Neuroarquitetura sem complicação, projetos comerciais, Home Relooking, Home Staging e os bastidores dos projetos. Um texto novo toda semana.', None)
    for c in cats:
        lst = [p for p in posts if p['category'] == c]
        paginate(lst, f'/blog/{slugify(c)}/', f'{c}: textos da Simone Afonso',
                 f'Textos sobre {c.lower()} escritos pela arquiteta Simone Afonso, com orientações práticas para casas e empresas.',
                 c, f'Todos os textos do blog sobre {c.lower()}.', c)

    # feeds e arquivos para buscadores e IAs
    today = dt.date.today().isoformat()
    urls = [(SITE + '/', today, None), (SITE + '/blog/', iso(posts[0]['modified'])[:10] if posts else today, None)]
    for c in cats:
        lst = [p for p in posts if p['category'] == c]
        urls.append((f'{SITE}/blog/{slugify(c)}/', iso(max(x['modified'] for x in lst))[:10], None))
    for p in posts:
        urls.append((SITE + p['path'], iso(p['modified'])[:10], SITE + p['cover'] if p['cover'] else None))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for u, lm, im in urls:
        sm.append(f'<url><loc>{esc(u)}</loc><lastmod>{lm}</lastmod>' + (f'<image:image><image:loc>{esc(im)}</image:loc></image:image>' if im else '') + '</url>')
    sm.append('</urlset>')
    write('sitemap.xml', '\n'.join(sm))

    feed = ['<?xml version="1.0" encoding="UTF-8"?>', '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/"><channel>',
            f'<title>{esc(CFG["name"])}</title><link>{SITE}/blog/</link><description>{esc(CFG["description"])}</description><language>pt-BR</language>',
            f'<atom:link href="{SITE}/blog/feed.xml" rel="self" type="application/rss+xml"/>']
    for p in posts[:30]:
        feed.append(f'<item><title>{esc(p["title"])}</title><link>{SITE}{p["path"]}</link><guid isPermaLink="true">{SITE}{p["path"]}</guid>'
                    f'<pubDate>{format_datetime(p["published"])}</pubDate><category>{esc(p["category"])}</category>'
                    f'<description>{esc(p["excerpt"] or p["answer"])}</description></item>')
    feed.append('</channel></rss>')
    write('blog/feed.xml', '\n'.join(feed))

    bots = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User', 'PerplexityBot', 'Perplexity-User', 'Google-Extended', 'Applebot-Extended', 'Bingbot']
    robots = 'User-agent: *\nAllow: /\n\n' + ''.join(f'User-agent: {b}\nAllow: /\n\n' for b in bots) + f'Sitemap: {SITE}/sitemap.xml\n'
    write('robots.txt', robots)

    llms = [f'# {CFG["name"]}', '', f'> {CFG["description"]}', '',
            f'{CFG["author"]} é {CFG["author_role"].lower()} em {CFG["locality"]} ({CFG["region"]}). Atende online e a domicílio, na Grande Vitória e em todo o Espírito Santo.', '',
            '## Páginas principais', f'- [Início]({SITE}/): serviços, projetos, depoimentos e contato.', f'- [Blog]({SITE}/blog/): um texto novo toda semana.', '',
            '## Textos do blog']
    for p in posts:
        llms.append(f'- [{p["title"]}]({SITE}{p["path"]}): {trunc(p["excerpt"] or p["answer"], 160)}')
    llms += ['', '## Contato', f'- WhatsApp: {CFG["phone"]}', f'- Instagram: {CFG["instagram"]}']
    write('llms.txt', '\n'.join(llms) + '\n')

    write('blog/posts.json', json.dumps([{
        'title': p['title'], 'category': p['category'], 'url': p['path'], 'image': p['cover'], 'alt': p['cover_alt'],
        'excerpt': trunc(p['excerpt'] or p['answer'], 140), 'date': iso(p['published'])[:10]} for p in posts[:12]], ensure_ascii=False))

    print(f'ok: {len(posts)} post(s), {len(cats)} categoria(s) -> {OUT}')


if __name__ == '__main__':
    main()
