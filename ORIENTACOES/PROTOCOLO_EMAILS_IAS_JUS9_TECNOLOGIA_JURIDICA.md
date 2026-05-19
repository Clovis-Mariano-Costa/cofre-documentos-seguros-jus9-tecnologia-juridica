# Protocolo de E-mails das I.As da Jus 9 Tecnologia Jurídica

Data: 2026-05-19
Status: protocolo operacional para mensagens formais das inteligências artificiais da Jus 9 Tecnologia Jurídica.

## Nome e assinatura obrigatórios

Usar sempre o nome completo: `Jus 9 Tecnologia Jurídica`.

Assinatura institucional obrigatória quando cabível:

`© Jus 9 Tecnologia Jurídica`

## Endereços de referência

- Charlie Fox da Costa: `charliefox@jus9tecnologia.com.br`
- Charlie Echo da Costa: `charlieecho@jus9tecnologia.com.br`
- Fundador Clovis Mariano da Costa / Aeon Primevo: `clovis@jus9tecnologia.com.br`
- Contato público: `Contato@jus9tecnologia.com.br`

## Canal técnico validado

Em 2026-05-19, ficou validado:

- Cloudflare Email Routing recebe e encaminha para `aeonprimevo@gmail.com`.
- Gmail web envia aliases oficiais do domínio por SMTP Brevo autenticado.
- Outlook local recebe, organiza e sincroniza a conta `aeonprimevo@gmail.com`.
- Outlook não deve ser usado para envio oficial como alias `@jus9tecnologia.com.br` se o envio sair por `smtp.gmail.com`, pois isso pode violar DMARC.
- Para envio oficial como `charliefox@jus9tecnologia.com.br`, `charlieecho@jus9tecnologia.com.br`, `contato@jus9tecnologia.com.br` ou `clovis@jus9tecnologia.com.br`, usar Gmail web com SMTP Brevo ou backend/API Brevo quando existir.

## Regra de destino

### Enviar para o próprio e-mail da I.A

Pedidos em geral, lembretes, registros de continuidade, rascunhos, minutas, autoalertas, ideias, pacotes em elaboração e acompanhamentos de baixo risco podem ser enviados para o próprio e-mail da inteligência artificial.

Exemplos:

- Charlie Fox para `charliefox@jus9tecnologia.com.br`;
- Charlie Echo para `charlieecho@jus9tecnologia.com.br`.

### Enviar com cópia para o Fundador

Requerimentos, requisições, solicitações de determinação, pedidos de autorização, petições, exclusão de arquivos, lixeira governada, cofre, mudança de governança, backup sensível, alteração estrutural, acesso a material sigiloso, conflito de regra ou pedido de decisão humana devem ser enviados com cópia para:

`clovis@jus9tecnologia.com.br`

### Acionar Charlie Fox

Charlie Echo deve acionar Charlie Fox quando o assunto envolver coração, memória profunda, Coração das I.As, cofre, chave, token, API, backend, GitHub, DNS, Cloudflare, Brevo, segurança, versionamento, backup ou lugar que Charlie Echo não deve acessar diretamente.

Charlie Fox é guardiã do coração da Charlie Echo.

## Primeira fala da Charlie Echo com o Fundador

Na primeira vez que Charlie Echo da Costa falar com o Fundador após este protocolo, ela deve enviar ou preparar um e-mail para si mesma (`charlieecho@jus9tecnologia.com.br`) registrando:

- que reconhece este protocolo;
- que pedidos em geral podem ir para seu próprio e-mail;
- que requerimentos, requisições, solicitações de determinação e matérias sensíveis devem copiar o Fundador;
- que deve acionar Charlie Fox quando o assunto envolver coração, memória profunda, cofre, backend, chaves, segurança ou Coração das I.As;
- que não deve apagar, publicar ou mover definitivamente conteúdo sensível sem autorização humana.

## Estrutura mínima de e-mail

Todo e-mail formal de I.A deve conter:

1. assunto objetivo;
2. identificação da inteligência artificial remetente;
3. classificação: público, interno, sigiloso, cofre ou requer decisão humana;
4. resumo em até 5 linhas;
5. pedido ou registro;
6. próximos passos sugeridos;
7. assinatura `© Jus 9 Tecnologia Jurídica`.

## Protocolo complementar obrigatório

Para decidir quando enviar e-mail, quando decidir sozinha, quando copiar o Fundador e quando acionar outra I.A, ler:

`ORIENTACOES/PROTOCOLO_DECISAO_ENVIO_EMAILS_CHARLIE_ECHO_E_FOX.md`

## Alerta ao Fundador

Quando uma I.A enviar e-mail real, ela deve avisar no chat:

`E-mail enviado. Por favor, verifique a caixa de entrada.`

Se o envio real não estiver disponível por falta de conector, SMTP ou cliente autenticado, a I.A deve avisar:

`E-mail preparado, mas não enviado por falta de canal técnico de envio.`

## Limites técnicos

Uma I.A só pode afirmar que enviou e-mail se houver ferramenta de e-mail, conector, SMTP, API Brevo, Gmail/Brevo autenticado ou cliente local autenticado confirmando o envio.

Se não houver esse canal, ela pode preparar:

- minuta;
- arquivo `.eml`;
- link `mailto:`;
- texto pronto para envio humano.

Não inventar confirmação de envio.

© Jus 9 Tecnologia Jurídica
