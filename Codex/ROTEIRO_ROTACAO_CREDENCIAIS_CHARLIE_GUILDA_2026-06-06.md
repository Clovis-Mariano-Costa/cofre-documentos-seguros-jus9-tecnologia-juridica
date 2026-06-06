# Roteiro de rotacao de credenciais - Charlie Guilda

Data: 2026-06-06
Classificacao: PUBLICO / SEGURANCA / SEM SEGREDOS
Responsavel humano: Clovis Mariano da Costa / Aeon Primevo
Codex responsavel: Charlie Fox da Costa

## Regra principal

Nao apagar segredo antigo antes de:

1. criar o novo segredo;
2. atualizar o ambiente que usa o segredo;
3. testar;
4. confirmar que o novo segredo funciona;
5. revogar o segredo antigo.

Nunca registrar neste arquivo o valor real de chave, token, senha, client secret, cookie secret ou `.env`.

## Estado visto em 2026-06-06

- OpenAI Platform mostra duas chaves ativas no projeto padrao:
  - `jus9-charlie-echo-transcri...`
  - `charlieecho-cloudflare`
- Ambas aparecem com permissao `Todos`. Preferir recriar com permissao restrita quando o uso permitir.
- O dominio `jus9tecnologia.com.br` aparece verificado no workspace OpenAI.
- O Cloudflare contem registros DNS de verificacao OpenAI, Google, Brevo, SPF, DKIM, DMARC e MX.
- Registros DNS de verificacao/e-mail nao sao tokens de API. Nao apagar esses registros sem necessidade especifica.
- Varredura local encontrou apenas `.env.example` no GitHub e nenhum `.env` real versionado.
- Apos troca do `OPENAI_API_KEY` no Cloudflare, a regressao publica `node tests/charlie-echo-public-regression.mjs` passou com `CHARLIE_ECHO_REGRESSION_OK`.

## Ordem recomendada

### 1. OpenAI Platform

1. Criar nova chave para producao da Charlie Echo / Cloudflare.
2. Nome sugerido: `jus9-charlie-echo-cloudflare-prod-2026-06`.
3. Se possivel, usar permissoes restritas somente para os endpoints usados pela Charlie Echo.
4. Atualizar o segredo no Cloudflare Pages/Workers.
5. Testar `https://charlieecho.jus9tecnologia.com.br/` e modulos principais.
6. Revogar as chaves antigas somente depois do teste passar.

Observacao: a API de analytics do Codex Enterprise deve usar chave separada, com escopo proprio, se e quando for usada. Nao misturar essa chave com a chave da Charlie Echo.

### 2. Cloudflare

Nao apagar registros DNS de verificacao antes de confirmar o impacto.

Rotacionar:

- `OPENAI_API_KEY`, se estiver em Pages/Workers secrets.
- `GOOGLE_CLIENT_ID`, quando recriado no Google OAuth.
- `GOOGLE_CLIENT_SECRET`, quando recriado no Google OAuth.
- `AUTH_COOKIE_SECRET`, com valor novo, longo e aleatorio.
- `JUS9_PUBLIC_ACCESS_TOKEN`, se o backend publico/local ainda usar.
- `CLOUDFLARE_API_TOKEN`, se houver token pessoal ou de deploy.

Preferir tokens Cloudflare com escopo minimo:

- token de DNS somente para a zona necessaria;
- token de Workers/Pages somente para deploy necessario;
- evitar token global da conta.

### 3. GitHub

1. Conferir Settings -> Secrets and variables -> Actions em repositorios que publicam ou chamam backend.
2. Substituir secrets antigos por novos.
3. Revogar personal access tokens antigos.
4. Preferir GitHub App, deploy key ou fine-grained PAT com repositorios especificos.
5. Nao colocar token em remoto Git; os remotes atuais verificados estao em formato HTTPS publico, sem token aparente.

### 4. Google OAuth

1. Criar ou rotacionar `GOOGLE_CLIENT_SECRET` no Google Cloud Console.
2. Manter redirect URIs exatamente iguais aos usados no backend/Cloudflare.
3. Atualizar Cloudflare/ambiente com `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET`.
4. Testar login antes de revogar segredo antigo.
5. Nao ativar SSO OpenAI sem concluir provedor de identidade e plano de retorno.

### 5. Apps Script - JUS9_DRIVE_SAVER_MVP

1. Abrir Project Settings -> Script Properties.
2. Trocar `CHAVE_INTERNA` por valor novo e forte.
3. Conferir IDs de pastas, URLs autorizadas e permissao do Web App.
4. Se o deploy mudar, atualizar a URL onde a Charlie Echo chamar o Apps Script.
5. Nao registrar `CHAVE_INTERNA` em GitHub, Drive publico ou chat.

### 6. E-mail: Brevo, Resend, SMTP

1. Gerar novas chaves/API/SMTP no provedor.
2. Atualizar backend ou Cloudflare secret correspondente.
3. Testar envio.
4. Revogar chave antiga.
5. Manter SPF, DKIM, DMARC e MX no Cloudflare, salvo se o provedor mandar novos registros.

### 7. Banco de dados

Se houver `DATABASE_URL` real em provedor:

1. criar nova senha/connection string;
2. atualizar backend;
3. testar leitura/escrita;
4. revogar a antiga.

Se nao houver banco real em uso, apenas manter `.env.example` como documentacao.

## Testes depois da rotacao

- `node tests/charlie-echo-public-regression.mjs` em `charlieecho-jus9-tecnologia-juridica`.
- Testar chat profissional, estudantes, MVP e downloads.
- Testar links externos oficiais.
- Testar OAuth/login se estiver ativo.
- Testar formulario/e-mail se houver chave Brevo/Resend.

## Fechamento seguro

Depois de tudo:

1. confirmar que nao ha `.env` real no GitHub;
2. confirmar que antigos tokens foram revogados;
3. registrar somente data e provedor rotacionado;
4. nunca registrar valores.
