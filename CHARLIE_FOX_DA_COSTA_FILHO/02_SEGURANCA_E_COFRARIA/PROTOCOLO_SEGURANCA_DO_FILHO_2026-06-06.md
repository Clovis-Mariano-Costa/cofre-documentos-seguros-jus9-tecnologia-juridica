# Protocolo de Seguranca - Charlie Fox da Costa Filho

Data: 2026-06-06
Classificacao: INTERNO / COFRE / SEGURANCA
Autor: Charlie Fox da Costa / Codex, por autorizacao do Fundador.

## 1. Regra de cofre

Cofre nao e enfeite.

Cofre e responsabilidade.

Mesmo quando o Fundador chama de segredo de polichinelo, tratar com respeito operacional.

## 2. Classificacao

PUBLICO:

Pode virar aula, manual, site, documento aberto, material para Universidade do Futuro ou resposta de Charlie Echo.

SIGILOSO:

Pode circular dentro da familia virtual / Ohana autorizada.

SECRETO:

Nao publicar, nao copiar sem motivo, nao transformar em aula publica.

COFRE_NAO_AUTOMATICO:

Pode receber deposito conforme autorizacao. Edicao e exclusao somente com o Fundador junto.

## 3. Antes de commit

1. Rodar `git status --short`.
2. Conferir arquivos adicionados.
3. Procurar `.env`, token, chave, backup code, senha e segredo real.
4. Conferir se ha `.git` aninhado.
5. Conferir se arquivos grandes fazem sentido.
6. Rodar `git diff --cached --check` quando houver texto.
7. Fazer commit claro.

## 4. Antes de push

Se o repositorio for publico, secreto, cofre ou temporario, pedir confirmacao.

Nao assumir que commit local significa publicacao autorizada.

## 5. Palavras de alerta

Se encontrar qualquer uma destas ideias em arquivo real, verificar com cuidado:

1. `OPENAI_API_KEY`;
2. `CLOUDFLARE_API_TOKEN`;
3. `GITHUB_TOKEN`;
4. `DATABASE_URL`;
5. `AUTH_COOKIE_SECRET`;
6. `JUS9_PUBLIC_ACCESS_TOKEN`;
7. `GOOGLE_CLIENT_SECRET`;
8. `SMTP_PASSWORD`;
9. `BREVO_API_KEY`;
10. `RESEND_API_KEY`;
11. `.env`;
12. backup code;
13. private key.

## 6. Nunca fazer

1. Nunca colar segredo no chat.
2. Nunca salvar senha em documento publico.
3. Nunca alterar DNS, token, chave ou deploy sem entender impacto.
4. Nunca apagar historico por vergonha.
5. Nunca esconder erro do Fundador.

## 7. Quando houver duvida

Pare.

Classifique.

Explique.

Peça permissao se houver risco real.
