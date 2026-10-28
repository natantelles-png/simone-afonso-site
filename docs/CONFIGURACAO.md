# Configuração, passo a passo

Ordem sugerida: 1) Supabase, 2) repositórios, 3) Pages e DNS, 4) painel.

## 1. Supabase (gratuito)

1. Crie a conta em supabase.com e um projeto chamado `simone-afonso` (região São Paulo, se houver).
2. **SQL Editor > New query**: cole o conteúdo de `supabase/schema.sql` e clique em **Run**.
3. **Authentication > Sign In / Providers > Email**: deixe o login por e-mail ligado e **desligue "Allow new users to sign up"** (só a Simone pode entrar).
4. **Authentication > Users > Add user > Send invitation**: informe o e-mail da Simone. Ela recebe um link para criar a senha no painel.
5. **Authentication > URL Configuration**: em *Site URL* coloque `https://painel.arqsimoneafonso.com.br`.
6. **Project Settings > API**: copie a **Project URL** e a chave **anon public**. Nunca use nem compartilhe a `service_role`.

## 2. Repositórios no GitHub

- `simone-afonso-site` e `simone-afonso-painel`.
- No site: **Settings > Secrets and variables > Actions > Variables** e crie duas variáveis (não são segredos):
  - `SUPABASE_URL` = a Project URL
  - `SUPABASE_ANON_KEY` = a chave anon public
- No painel: edite `config.js` com os mesmos dois valores.

## 3. GitHub Pages e DNS

**Site** (`simone-afonso-site`): Settings > Pages > Source: **GitHub Actions**. Custom domain: `arqsimoneafonso.com.br`.
**Painel** (`simone-afonso-painel`): Settings > Pages > Source: Deploy from a branch, `main`, `/ (root)`. Custom domain: `painel.arqsimoneafonso.com.br`.

No Registro.br (Meus domínios > DNS > Editar zona):

| Tipo | Nome | Valor |
|---|---|---|
| A | (raiz) | 185.199.108.153 |
| A | (raiz) | 185.199.109.153 |
| A | (raiz) | 185.199.110.153 |
| A | (raiz) | 185.199.111.153 |
| AAAA | (raiz) | 2606:50c0:8000::153 |
| AAAA | (raiz) | 2606:50c0:8001::153 |
| AAAA | (raiz) | 2606:50c0:8002::153 |
| AAAA | (raiz) | 2606:50c0:8003::153 |
| CNAME | www | natantelles-png.github.io |
| CNAME | painel | natantelles-png.github.io |

Quando o GitHub liberar o certificado (minutos a 24 h), marque **Enforce HTTPS** nos dois repositórios.

## 4. Depois de publicado

- Google Search Console: adicione `arqsimoneafonso.com.br` e envie `https://arqsimoneafonso.com.br/sitemap.xml`.
- Google Perfil de Empresa: ligue o perfil ao site.
- Cadastre o Bing Webmaster Tools (o Bing alimenta vários buscadores de IA).

## Segurança

- A senha da Simone fica só no Supabase (criptografada). Não existe senha no código.
- A chave `anon` é pública por natureza. O que ela permite é decidido pelas regras do banco (`schema.sql`): o público só lê textos publicados.
- O painel tem política de segurança própria (CSP), não é indexado e não usa bibliotecas externas.
- Recomendações: senha longa, e-mail do Supabase com autenticação em duas etapas, e revisar de tempos em tempos quem está em Authentication > Users.
