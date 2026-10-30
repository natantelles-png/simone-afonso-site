import re, base64, json, mimetypes, os, sys, shutil, hashlib
import os
S=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
src=open(S+'source/Main.dc.html',encoding='utf-8').read()
M={
'9b6e17901bbd981ee054c7f2091e6b11':'assets/out/logo_plum.png','8549e41ff079b3b7ba922120046d8968':'assets/out/logo_white.png',
'171e1b576855467a0b55f227a76915d0':'assets/out/tex_ameixa.jpg','88c7b3a49ccaef72fd41208cd3726bc6':'assets/out/tex_rose.jpg','522dbe99eb7f6c25000fe726a3f1df4c':'assets/out/tex_papel.jpg',
'96c3ee090179800998085b94a50fe70a':'assets/out3/pattern_ameixa.svg','d40ed56784d9fb5dc1b476838607285e':'assets/out3/pattern_rose.svg',
'51a49737b796e9aeed3575366f1c82bd':'assets/out/selo.jpg','0d85a914b8915e26f41dca4b450c32c0':'assets/out3/timbrado.jpg','0fd1279c8eab9538a3b3011aadde6d90':'assets/out4/simone_hero.webp',
'2f720a05d6a9253e593016f108b1408c':'assets/out/s_verde.jpg','1223a803a7dcf9c5f48b5711c74679d6':'assets/out/s_estante.jpg','6c624862dc99203b6c7a6381962a0312':'assets/out/s_contato.jpg','44ff8751e58f4855ad9b6233372f783f':'assets/out/s_palco1.jpg',
'6a5444c6eff9319e829e4b113dfe3df2':'assets/out/ad_menina_antes.jpg','cecba3083e683cb18d22803fa5d7beaa':'assets/out/ad_menina_depois.jpg',
'368ed813c9324c0da7ac4660dcab5076':'assets/out/ad_compacta_antes.jpg','33f4feb7c2c9db4e3e30a3b9c2a5b2cb':'assets/out/ad_compacta_depois.jpg',
'd24bfac980f14d8293324031094a6267':'assets/out/ad_banho_antes.jpg','520dd457bb0db10dd2d81020750116c9':'assets/out/ad_banho_depois.jpg',
'a456a8ca596f7ad2bc0ef441832e76eb':'assets/out/ad_cozinha_antes.jpg','7ed70dd2abb91f069f69a818a554120e':'assets/out/ad_cozinha_depois.jpg',
'2c0278b1b977f0a5394d5ea41133231b':'assets/out/ad_sala_antes.jpg','304a9c36eacce5c833f0a5c03118139e':'assets/out/ad_sala_depois.jpg',
'8baff990668af6c844055f2155ed99c7':'assets/out/p_bebe.jpg','9434ca6f7a75982c384e53bcb16eed7f':'assets/out/p_bemmequer.jpg','52279fc09952a84c7317262bc50a3868':'assets/out/p_bicho1.jpg',
'ba252cbf837e95af27546e745de38b5a':'assets/out/p_bicho2.jpg','0fbbf64c2495910f72e5f9d29d86bfda':'assets/out/p_bicho3.jpg','502873f8613924c8d1def68201c4fce2':'assets/out/p_coz1.jpg',
'f4b216132f25d0ae2347a15b0cec8230':'assets/out/p_coz2.jpg','cdf2f82aa62c27f0b88eb904dffdb89d':'assets/out3/p_jantar2.jpg','fe931523e0b7d5f57a0b6aa5b598216a':'assets/out/p_kit1.jpg',
'f4348f9a1223fe5813c56034f71c1902':'assets/out/p_kit2.jpg','78c989c74bc91c01f23324e6a0f364fd':'assets/out/p_kit3.jpg','82fad9013dc3427d3b0a6ee57f646553':'assets/out/p_menina.jpg',
'8c67ed1d9eb5f458986765b5c8df2479':'assets/out/p_nichos.jpg','246c5f1719c5ce2ff6398011052f76de':'assets/out/p_toca1.jpg','a8b489b87bcf1eb2a029ea77e60c624a':'assets/out/p_toca2.jpg',
'5774a269719d52b2f7220f6de29b5bf7':'assets/out/p_tv.jpg','b0fb4a1f49cfae1c2ee5c96544df148d':'assets/out3/p_suite.jpg','196d9a124d810babc22294161c1f7e48':'assets/out3/p_varanda.jpg',
'751e2d2705d8d090bc98f64dfc5d32e8':'assets/out3/p_vdb1.jpg','bbefd20c1aab93e2b82827005851e059':'assets/out3/p_vdb2.jpg',
'6d44d7539ebad1040e472dfb2cdefb31':'assets/out5/p_bmq12.jpg','cc43166d60bf5c0e30a949c4e8dbbc1d':'assets/out5/p_bmq13.jpg','dff9d905883527232e1267d4a6fa515e':'assets/out5/p_multi_jantar.jpg','579d150e09e2dfa0b0963998da372229':'assets/out5/p_multi_estar.jpg','5578f91be29d035d93552ff1a278b645':'assets/out5/p_stand.jpg',
'2bdd09356c6cde853e048983509204f3':'assets/fonts/adventor-regular.woff','7f9c3b609f7cecb166a6905d796a525f':'assets/fonts/adventor-italic.woff','fd07e328acb7b6f8a82a42de7a20fc31':'assets/fonts/adventor-bold.woff','87f88cf08107b03ae6bc8a6aca4f45d7':'assets/fonts/adventor-bolditalic.woff'}
for _f in os.listdir(S+'assets/v2'): M[os.path.splitext(_f)[0]]='assets/v2/'+_f
ids=set(re.findall(r'/_blob/([0-9a-f]{32})',src))
missing=ids-set(M); assert not missing, missing
M={k:v for k,v in M.items() if k in ids}

MODE='standalone' if '--standalone' in sys.argv else 'site'
SITE_URL='https://arqsimoneafonso.com.br'
HOME=S+'_home/'
if MODE=='site':
    shutil.rmtree(HOME,ignore_errors=True); os.makedirs(HOME+'img')
img={}
for i in ids:
    p=S+M[i]
    if MODE=='standalone':
        mt=('font/woff' if p.endswith('.woff') else mimetypes.guess_type(p)[0]) or ('image/webp' if p.endswith('webp') else 'application/octet-stream')
        img[i]='data:%s;base64,%s'%(mt,base64.b64encode(open(p,'rb').read()).decode())
    else:
        ext=os.path.splitext(p)[1].lower()
        name=i[:12]+ext; shutil.copy(p,HOME+'img/'+name); img[i]='/img/'+name
m=re.search(r'<title>(.*?)</title>',src,re.S); title=m.group(1)
x=re.search(r'<x-dc>(.*)</x-dc>',src,re.S).group(1)
helm=re.search(r'<helmet>(.*?)</helmet>',x,re.S).group(1)
body=x.replace('<helmet>'+helm+'</helmet>','')
css='\n'.join(re.findall(r'<style>(.*?)</style>',helm,re.S))
link=re.search(r'<link[^>]*>',helm).group(0)
script=re.search(r'<script type="text/x-dc"[^>]*>(.*?)</script>',src,re.S).group(1)
assert '</script' not in body and '</script' not in script
runtime=open(S+'build/runtime.js',encoding='utf-8').read()
inline='\nconst IMG='+json.dumps(img)+';\n'+runtime+'\n'+script+'\nboot(Component);\n'
h=base64.b64encode(hashlib.sha256(inline.encode('utf-8')).digest()).decode()
cfg=json.load(open(S+'blog/config.json',encoding='utf-8'))
if MODE=='site':
    csp=("default-src 'none'; script-src 'sha256-"+h+"'; style-src 'unsafe-inline' https://fonts.googleapis.com; "
         "font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; media-src 'self'; connect-src 'self'; form-action 'none'; base-uri 'none'; object-src 'none'; upgrade-insecure-requests")
else:
    csp=("default-src 'none'; script-src 'sha256-"+h+"'; style-src 'unsafe-inline' https://fonts.googleapis.com; "
         "font-src data: https://fonts.gstatic.com; img-src data:; connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'; upgrade-insecure-requests")
desc=cfg['description']
seo=''
if MODE=='site':
    ld={'@context':'https://schema.org','@graph':[
      {'@type':'Person','@id':SITE_URL+'/#simone','name':cfg['author'],'jobTitle':cfg['author_role'],'url':SITE_URL+'/','image':SITE_URL+'/blog/assets/simone.jpg','sameAs':[cfg['instagram']],'knowsAbout':cfg['knows_about'],'worksFor':{'@id':SITE_URL+'/#negocio'}},
      {'@type':['ProfessionalService','LocalBusiness'],'@id':SITE_URL+'/#negocio','name':cfg['name'],'url':SITE_URL+'/','logo':SITE_URL+'/blog/assets/logo-ameixa.png','image':SITE_URL+'/og.jpg','telephone':cfg['phone'],'description':cfg['description'],'founder':{'@id':SITE_URL+'/#simone'},'sameAs':[cfg['instagram']],'areaServed':[{'@type':'AdministrativeArea','name':'Espírito Santo'},{'@type':'City','name':'Vitória'}],'address':{'@type':'PostalAddress','addressLocality':cfg['locality'],'addressRegion':cfg['region'],'addressCountry':'BR'},'knowsAbout':cfg['knows_about'],'priceRange':'$$'},
      {'@type':'WebSite','@id':SITE_URL+'/#site','url':SITE_URL+'/','name':cfg['name'],'inLanguage':'pt-BR','publisher':{'@id':SITE_URL+'/#negocio'}},
      {'@type':'WebPage','@id':SITE_URL+'/#pagina','url':SITE_URL+'/','name':'Simone Afonso | Arquitetura de interiores e neuroarquitetura em Vitória (ES)','isPartOf':{'@id':SITE_URL+'/#site'},'about':{'@id':SITE_URL+'/#negocio'},'inLanguage':'pt-BR'}]}
    ttl='Simone Afonso | Arquitetura de interiores e neuroarquitetura em Vitória (ES)'
    seo=f"""<link rel="canonical" href="{SITE_URL}/">
<link rel="icon" href="/favicon.png" type="image/png">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta property="og:locale" content="pt_BR"><meta property="og:type" content="website"><meta property="og:site_name" content="{cfg['name']}">
<meta property="og:title" content="{ttl}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{SITE_URL}/"><meta property="og:image" content="{SITE_URL}/og.jpg">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{ttl}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{SITE_URL}/og.jpg">
<meta name="theme-color" content="#534243">
<link rel="alternate" type="application/rss+xml" title="{cfg['name']}" href="{SITE_URL}/blog/feed.xml">
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False,separators=(',',':'))}</script>"""
    title=ttl
else:
    desc="Prévia do site de Simone Afonso, arquiteta de interiores e neuroarquiteta em Vitória (ES)."
html=f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{csp}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{title}</title>
<meta name="description" content="{desc}">
{seo}
{link}
<style id="app-css">/*CSS*/</style>
</head>
<body>
<div id="app"></div>
<script type="text/plain" id="tpl">{body}</script>
<script type="text/plain" id="css-src">{css}</script>
<script>{inline}</script>
</body>
</html>"""
out=(HOME+'index.html') if MODE=='site' else S+'previa-standalone.html'
open(out,'w',encoding='utf-8').write(html)
print(MODE,len(html)/1e6,'MB ->',out)
