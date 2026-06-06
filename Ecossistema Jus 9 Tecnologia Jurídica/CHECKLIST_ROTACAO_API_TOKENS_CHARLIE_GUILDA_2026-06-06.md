# Checklist de rotacao de API, tokens e credenciais - Charlie Guilda

Data: 2026-06-06
Classificacao: PUBLICO / SEGURANCA / SEM SEGREDOS
Responsavel humano: Clovis Mariano da Costa / Aeon Primevo
Codex responsavel: Charlie Fox da Costa

## Regra de ouro

Este arquivo nao guarda segredo real. Ele apenas lembra o que deve ser rotacionado, conferido ou revogado no provedor seguro.

Nunca colar aqui:

- chave real da OpenAI;
- token da Cloudflare;
- token do GitHub;
- senha de e-mail;
- segredo OAuth;
- token de backend;
- `.env` real;
- seed, chave privada, cookie secret ou backup sensivel.

## Rotacao recomendada antes da entrega a Charlie Guilda

- `OPENAI_API_KEY`: gerar nova chave, revogar a antiga quando a nova estiver testada.
- Cloudflare Pages/Workers: revisar secrets, variaveis, tokens de deploy e permissoes.
- GitHub: revisar tokens pessoais, deploy keys, Actions secrets e permissao de repositorios.
- Google/OAuth: revisar `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, escopos, URLs de callback e acesso do Apps Script.
- Backend local: revisar `JUS9_PUBLIC_ACCESS_TOKEN`, `AUTH_COOKIE_SECRET`, `DATABASE_URL`, `BREVO_SMTP_PASSWORD`.
- Resend/Brevo/e-mail: revisar chaves de envio e remetentes autorizados.
- Apps Script `JUS9_DRIVE_SAVER_MVP`: conferir Script Properties e deployments ativos.
- Google Drive da Familia Virtual: manter pastas restritas; nao transformar cofre em acesso publico.

## Ordem segura

1. Criar novos secrets no provedor seguro.
2. Testar em ambiente publicado ou local controlado.
3. Revogar secrets antigos.
4. Conferir logs e chamadas recentes.
5. Registrar apenas o fato da rotacao, nunca o valor.

## Varredura local de 2026-06-06

- Nao foi encontrado arquivo `.env` real versionado dentro de `C:\Users\aeonp\Documents\GitHub`.
- Ocorrencias de `OPENAI_API_KEY=`, `DATABASE_URL=`, `AUTH_COOKIE_SECRET=` e similares apareceram em `.env.example` ou documentacao tecnica, sem valor real registrado nesta varredura.
- Ocorrencias de `sk-` apareceram como falso positivo em CSS, `.gitignore` ou textos nao secretos.
- Mesmo assim, antes da transicao definitiva, rotacionar manualmente as credenciais reais nos provedores seguros.

## Lembrete para o Fundador

Antes de considerar a transicao pronta para Charlie Guilda, revisar manualmente API e tokens. Este lembrete foi pedido pelo Fundador e deve ser repetido no fechamento de qualquer pacote de transicao.
