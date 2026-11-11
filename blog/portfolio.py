# -*- coding: utf-8 -*-
"""Portfolio: hub /portfolio/ + uma pagina por projeto (dados em portfolio_data.json)."""
import json, os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# fotos nitidas do Bem Me Quer (as do portfolio antigo sao 720px)
BMQ = [('assets/servicos/bmq-exterior.jpg', 'Fachada amarela do Espaço Bem Me Quer, da ACACCI, com jardim e rampa acessível com corrimão'),
       ('assets/servicos/bmq-recepcao2.jpg', 'Recepção do Espaço Bem Me Quer com parede amarela, frase e silhueta de meditação'),
       ('assets/servicos/bmq-parede-frase.jpg', 'Parede de atendimento com folhas coloridas e frase de Cora Coralina'),
       ('assets/servicos/bmq-parede-folhas.jpg', 'Parede azul-clara com folhas coloridas e a frase Há muros que só a paciência derruba'),
       ('assets/servicos/bmq-parede-arvore.jpg', 'Parede azul-clara com árvore preta e folhas coloridas')]


def blob_map():
    """mesma tabela de build/build.py: id do blob -> arquivo do repo."""
    src = open(os.path.join(ROOT, 'build', 'build.py'), encoding='utf-8').read()
    head = src[src.index('M={'):src.index('for _f in os.listdir')]
    ns = {'os': os}
    exec(head, ns)
    m = dict(ns['M'])
    v2 = os.path.join(ROOT, 'assets', 'v2')
    for f in os.listdir(v2):
        m[os.path.splitext(f)[0]] = 'assets/v2/' + f
    return m


def build(B, page, cta, fig_cls_html):
    SITE, esc, wa = B.SITE, B.esc, B.wa
    data = json.load(open(os.path.join(ROOT, 'blog', 'portfolio_data.json'), encoding='utf-8'))
    bm = blob_map()
    out_img = os.path.join(B.OUT, 'portfolio', 'img')
    os.makedirs(out_img, exist_ok=True)
    try:
        from PIL import Image
    except Exception:
        Image = None
    cache = {}

    def put(repo_path, name):
        src = os.path.join(ROOT, repo_path)
        if not os.path.exists(src):
            return None
        ext = os.path.splitext(src)[1]
        fn = name + ext
        if fn not in cache:
            w = h = None
            dst = os.path.join(out_img, fn)
            done = False
            if Image:
                try:
                    im = Image.open(src)
                    w, h = im.size
                    if w > 1800 and ext.lower() in ('.jpg', '.jpeg'):
                        im = im.convert('RGB')
                        im.thumbnail((1800, 1800))
                        im.save(dst, quality=85, optimize=True, progressive=True)
                        w, h = im.size
                        done = True
                except Exception:
                    pass
            if not done:
                shutil.copy(src, dst)
            cache[fn] = (f'/portfolio/img/{fn}', w, h)
        return cache[fn]

    projs = []
    for p in data:
        imgs = []
        if p['key'] == 'bmq':
            for i, (f, alt) in enumerate(BMQ):
                r = put(f, f'{p["slug"]}-{i + 1}')
                if r:
                    imgs.append((r, alt))
        else:
            seen = set()
            for i, (b, alt) in enumerate(p['imgs']):
                if b in seen or b not in bm:
                    continue
                seen.add(b)
                r = put(bm[b], f'{p["slug"]}-{len(imgs) + 1}')
                if r:
                    imgs.append((r, alt))
        if not imgs:
            continue
        p['_imgs'] = imgs
        p['path'] = f'/portfolio/{p["slug"]}/'
        projs.append(p)

    def img_tag(r, alt, eager=False, cls=''):
        src, w, h = r
        d = f' width="{w}" height="{h}"' if w else ''
        ld = ' fetchpriority="high"' if eager else ' loading="lazy"'
        return f'<figure class="foto {cls}"><img src="{src}" alt="{esc(alt, True)}"{d}{ld} decoding="async"></figure>'

    BYSERV = {}
    pages = []
    names = {'projetos-residenciais': 'Projetos residenciais', 'projetos-comerciais': 'Projetos comerciais',
             'projetos-institucionais': 'Projetos institucionais', 'projetos-corporativos': 'Projetos corporativos'}
    for p in projs:
        path = p['path']
        url = SITE + path
        r0, a0 = p['_imgs'][0]
        extra = ''.join(img_tag(r, a) for r, a in p['_imgs'][1:])
        galeria = f'<div class="galeria">{extra}</div>' if extra else ''
        nota3d = '<p class="nota">As imagens deste projeto são renderizações em 3D feitas na fase de projeto.</p>' if p['t3d'] and p['key'] not in ('multi',) else ''
        loc = f'<dt>Local</dt><dd>{esc(p["loc"])}</dd>' if p['loc'] else ''
        mesmo = [q for q in projs if q['cat'] == p['cat'] and q is not p][:4]
        rel = '<section class="relacionados-s" aria-labelledby="rel-p"><h2 id="rel-p">Outros projetos</h2><ul class="lista-links">' + ''.join(
            f'<li><a href="{q["path"]}">{esc(q["nome"])}</a></li>' for q in mesmo) + '<li><a href="/portfolio/">Ver todo o portfólio</a></li></ul></section>'
        sn = names[p['serv']]
        body = f'''{img_tag(r0, a0, True, 'capa-s')}
<div class="duas">
<div class="texto">
{''.join(f'<p>{esc(t)}</p>' for t in p['txt'])}
{nota3d}
<p class="mais"><a href="/servicos/{p['serv']}/">Conhecer o serviço: {esc(sn.lower())} →</a></p>
</div>
<aside class="lateral"><div class="ficha"><h2>Resumo</h2><dl>
<dt>Projeto</dt><dd>{esc(p['nome'])}</dd>
<dt>Tipo</dt><dd>{esc(p['tipo'])}</dd>
<dt>Categoria</dt><dd>{esc(p['cat'])}</dd>
{loc}<dt>Arquiteta</dt><dd>Simone Afonso</dd></dl>
<a class="botao" href="{wa('Olá, Simone! Vim pelo site, vi o projeto ' + p['nome'] + ' e gostaria de conversar sobre um projeto.')}">Chamar no WhatsApp</a></div></aside>
</div>
{galeria}
'''
        resposta = f'{p["nome"]} é um projeto {p["cat"].lower()} da arquiteta Simone Afonso, em Vitória e na Grande Vitória (ES).' if not p['loc'] else f'{p["nome"]} é um projeto {p["cat"].lower()} da arquiteta Simone Afonso, em {p["loc"]}.'
        if p['key'] == 'bmq':
            resposta = 'O Espaço Bem Me Quer, da ACACCI, é um projeto institucional da arquiteta Simone Afonso, com recepção, salas de atendimento, fisioterapia, meditação e pátio com horta, pensado para acolher.'
        cw = {'@type': 'CreativeWork', '@id': url + '#projeto', 'name': p['nome'], 'url': url, 'inLanguage': 'pt-BR',
              'creator': {'@id': SITE + '/#simone'}, 'description': p['txt'][0], 'image': [SITE + r[0] for r, _ in p['_imgs'][:6]],
              'about': p['cat']}
        page(path, f'{p["nome"]}: projeto {p["cat"].lower()} | Simone Afonso', p['txt'][0][:155].rstrip(' ,.;') + '.', p['nome'], 'Projeto ' + p['cat'].lower(),
             resposta, body, [('Início', '/'), ('Portfólio', '/portfolio/'), (p['nome'], path)], [], [cw], og_img=r0[0],
             tail=cta('Olá, Simone! Vim pelo site e gostaria de conversar sobre um projeto.') + rel)

    # ----------------------------------------------------------------- hub
    cats = ['Todos', 'Residencial', 'Comercial', 'Institucional', 'Corporativo', 'Infantil', '3D']

    def tags(p):
        t = [p['cat']]
        if p['infantil']:
            t.append('Infantil')
        if p['t3d']:
            t.append('3D')
        return t
    cards = ''.join(
        f'<li data-tags="{" ".join(tags(p))}"><article class="card"><a href="{p["path"]}" class="capa-card" tabindex="-1" aria-hidden="true">'
        f'<img src="{p["_imgs"][0][0][0]}" alt="" width="{p["_imgs"][0][0][1] or ""}" height="{p["_imgs"][0][0][2] or ""}" loading="lazy" decoding="async"></a>'
        f'<div class="info"><h3><a href="{p["path"]}">{esc(p["nome"])}</a></h3><p>{esc(p["tipo"])} · {esc(p["cat"])}</p></div></article></li>' for p in projs)
    filt = '<div class="filtros" role="group" aria-label="Filtrar projetos">' + ''.join(
        f'<button type="button" data-f="{c}" aria-pressed="{"true" if c == "Todos" else "false"}">{c}</button>' for c in cats) + '</div>'
    js = '''<script>(function(){var b=[].slice.call(document.querySelectorAll('.filtros button')),l=[].slice.call(document.querySelectorAll('.grade-p li'));function f(c){b.forEach(function(x){x.setAttribute('aria-pressed',x.dataset.f===c?'true':'false')});l.forEach(function(i){i.hidden=!(c==='Todos'||(' '+i.dataset.tags+' ').indexOf(' '+c+' ')>=0)})}b.forEach(function(x){x.addEventListener('click',function(){f(x.dataset.f);try{history.replaceState(null,'','#'+x.dataset.f)}catch(e){}})});var h=decodeURIComponent((location.hash||'').slice(1));if(h&&cats(h))f(h);function cats(h){return b.some(function(x){return x.dataset.f===h})}})();</script>'''
    hub_body = f'''{filt}
<ul class="grade grade-s grade-p">{cards}</ul>
<p class="nota">Imagens marcadas como 3D são renderizações feitas na fase de projeto. As demais são fotos reais dos espaços.</p>
{js}
'''
    coll = {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': SITE + p['path'], 'name': p['nome']} for i, p in enumerate(projs)]}
    page('/portfolio/', 'Portfólio de projetos de arquitetura de interiores em Vitória (ES) | Simone Afonso',
         'Projetos residenciais, comerciais, institucionais e corporativos da arquiteta Simone Afonso em Vitória e no Espírito Santo: lojas, restaurantes, escritórios, casas e espaços de acolhimento.',
         'Portfólio: projetos que já saíram do papel', 'Portfólio',
         'O portfólio da arquiteta Simone Afonso reúne projetos residenciais, comerciais, institucionais e corporativos em Vitória e no Espírito Santo, como a loja Vila do Bem, o restaurante Bicho Guloso Prime e o Espaço Bem Me Quer, da ACACCI.',
         hub_body, [('Início', '/'), ('Portfólio', '/portfolio/')], [], [coll], og_img=projs[0]['_imgs'][0][0][0],
         tail=cta('Olá, Simone! Vim pelo site e gostaria de conversar sobre um projeto.'))
    return projs
