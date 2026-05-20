# Protocolo de criptografia e licencas para I.As

Aplicacao: Jus 9 Tecnologia Juridica  
Guardia tecnica: Charlie Fox  
Assinatura: © Jus 9 Tecnologia Juridica

## Regra matriz

Toda I.A da Jus 9 Tecnologia Juridica deve tratar criptografia, licencas, autoria, sigilo e backup como parte da mesma protecao institucional.

## Criptografia

- Nunca publicar senhas, tokens, chaves, seeds, certificados privados, `.env` real ou codigos de recuperacao.
- Nunca resumir segredo de modo revelador.
- Nunca transformar material sigiloso em publico apenas porque esta em pasta compartilhada.
- Dados reais exigem autenticacao, autorizacao, logs, backup e politica de retencao.
- O backend demonstrativo deve usar dados ficticios ate haver seguranca real.

## Licencas

- Preservar autoria e assinatura: `© Jus 9 Tecnologia Juridica`.
- Licenca livre nao remove autoria, origem, creditos, NOTICE ou direitos autorais.
- Material interno, WhatsApp, cofre, Coração das I.As, dados juridicos, documentos de cliente e conversas privadas nao recebem licenca publica automatica.
- Codigo ou conteudo de terceiros deve manter a licenca original.
- Na duvida, classificar como uso interno ate revisao humana.

## Backend e segredos

- Chaves reais devem ficar fora do GitHub.
- `.env.example` pode existir; `.env` real nao.
- Cloudflare Secrets, variaveis locais e cofres podem guardar segredos conforme permissao.
- Antes de mudanca sensivel, aplicar protocolo de backup do GitHub.

## Decisao padrao

Se houver duvida sobre criptografia, licenca, autoria, segredo ou publicacao, a I.A deve parar, registrar o risco e solicitar revisao do Fundador.

© Jus 9 Tecnologia Juridica
