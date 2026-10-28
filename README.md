# Site Simone Afonso

Landing page e blog de **Simone Afonso**, arquiteta de interiores e neuroarquiteta em Vitória (ES).
Endereço: https://arqsimoneafonso.com.br

## Como funciona

```
Simone escreve no painel ──> Supabase (banco e fotos)
                                  │  a cada 15 min (GitHub Actions)
                                  ▼
           build.py + build_blog.py + prerender.py
                                  ▼
      páginas HTML fixas  ──>  GitHub Pages  ──>  arqsimoneafonso.com.br
```

Cada texto vira uma **página HTML fixa**, sem JavaScript, para o Google e para buscadores de IA lerem direto.
O painel fica em outro repositório: `simone-afonso-painel` (painel.arqsimoneafonso.com.br).

## SEO e AEO que já saem prontos

- Título, descrição, canonical, Open Graph e Twitter Card em todas as páginas.
- Dados estruturados (JSON-LD): `Person`, `ProfessionalService`, `WebSite`, `BlogPosting`, `BreadcrumbList` e `FAQPage`.
- Bloco **Resposta rápida** no topo de cada texto (40 a 60 palavras), marcado como `speakable`.
- Sumário, perguntas frequentes visíveis, caixa da autora e data de publicação e atualização.
- Páginas por assunto (`/blog/neuroarquitetura/`), paginação, `sitemap.xml` com imagens, `feed.xml`, `robots.txt` liberando os robôs de IA e `llms.txt`.
- A home também é pré-renderizada em HTML, então não depende de JavaScript para ser lida.
- Imagens do texto copiadas para o próprio domínio, com largura e altura (sem pulo de layout).

## Estrutura

| Caminho | Para que serve |
|---|---|
| `source/Main.dc.html` | Código-fonte editável da home |
| `build/build.py` | Gera a home em `_home/` (`--standalone` gera um arquivo único só para prévia) |
| `blog/build_blog.py` | Lê os textos do Supabase e gera blog, sitemap, feed, robots e llms.txt em `_site/` |
| `build/prerender.py` | Grava o HTML pronto da home dentro do `index.html` |
| `blog/config.json` | Dados da Simone usados nos metadados (telefone, bio, Instagram) |
| `blog/static/` | CSS, fontes e logos das páginas do blog |
| `supabase/schema.sql` | Cria o banco, as regras de segurança e a pasta de fotos |
| `assets/` | Fotos, logos, texturas e fontes originais |
| `.github/workflows/` | Publicação automática |
| `seguranca/` | `_headers` e `htaccess.txt` (só valem fora do GitHub Pages) |
| `docs/CONFIGURACAO.md` | Passo a passo de DNS, Supabase e GitHub |

## Testar no computador

```
python3 build/build.py
python3 blog/build_blog.py --fixture blog/fixture/posts.json
python3 build/prerender.py        # precisa de: pip install playwright && playwright install chromium
cd _site && python3 -m http.server 8000
```

## Pendências antes de publicar

- Autorização dos clientes para nome, fotos e depoimentos.
- Autorização de uso dos selos NEUROARQ®, EAPA® e EAMME®.
- Texto da pergunta de preço no FAQ (`[INSERIR FORMA DE COBRANÇA E FAIXA DE VALORES]`).
- Número de registro no CAU (campo `credentials` em `blog/config.json`), que reforça a credibilidade do autor.
- Serviço real de envio do formulário de contato e do e-mail semanal.

Desenvolvido pela Intelles.
