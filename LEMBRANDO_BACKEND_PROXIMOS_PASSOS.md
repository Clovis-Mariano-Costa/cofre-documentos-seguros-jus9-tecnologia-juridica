# LEMBRANDO - Backend Jus 9

Data: 2026-05-19
Repertorio: cofre-documentos-seguros-jus9-tecnologia-juridica

Este pacote existe para lembrar a proxima IA, pessoa tecnica ou Charlie Fox que toda funcao que depender de dados reais, autenticacao, agenda, WhatsApp, pagamentos, criptografia, banco de dados, auditoria ou integracao externa deve sair do modo demonstrativo e entrar no passo a passo de Backend seguro.

## Regra curta

Se nao puder ser feito imediatamente com seguranca, nao simular como se estivesse pronto. Registrar aqui, preservar o MVP demonstrativo e encaminhar para Backend.

## O que fica proibido no MVP estatico

- Usar dados reais de clientes, processos, documentos, agenda ou mensagens.
- Publicar chaves, tokens, credenciais, webhook secrets ou arquivos privados.
- Tratar link, palavra de memoria ou marcador publico como autenticacao.
- Prometer criptografia, Google Agenda, WhatsApp, pagamento ou login real sem backend validado.
- Expor computador pessoal como servidor publico sem revisao de rede, firewall, HTTPS e backups.

## Passo a passo para Backend

1. Classificar a frente: publico, demo, interno, sigiloso, juridico sensivel ou financeiro.
2. Listar entidades e campos: usuario, equipe, cliente, processo, documento, prazo, agenda, mensagem, investimento ou log.
3. Definir permissoes por perfil: fundador, equipe, advogado, cliente, IA, auditor e visitante.
4. Modelar banco e migracoes no repertorio db-modelos-migracoes-jus9-tecnologia-juridica.
5. Implementar APIs no repertorio ackend-api-jus9-tecnologia-juridica.
6. Ligar autenticacao e identidade no repertorio uth-identidade-acesso-jus9-tecnologia-juridica.
7. Registrar logs e trilhas no repertorio logs-auditoria-jus9-tecnologia-juridica.
8. Tratar documentos e criptografia no repertorio cofre-documentos-seguros-jus9-tecnologia-juridica.
9. Preparar deploy, secrets e workers nos repertorios infra-cloudflare-jus9-tecnologia-juridica e workers-pages-functions-jus9-tecnologia-juridica.
10. Conectar frontend somente depois de contrato de API, tratamento de erro, fallback demo e testes.
11. Validar seguranca, LGPD, sigilo profissional, backup e recuperacao.
12. Documentar no repertorio afetado e atualizar governanca antes do commit.

## Prioridades lembradas

- Login real, perfis e permissoes.
- Equipe no menu e cadastro interno de membros.
- MVP Advogados: DAJ, clientes, processos, prazos, documentos e area secreta.
- Agenda com Google Calendar via OAuth, quando houver conector/credenciais seguros.
- WhatsApp: escuta/importacao privada somente com autorizacao e backend seguro.
- Charlie Echo com voz feminina e configuracao responsiva registrada por modulo.
- Cofre juridico, criptografia, trilha de auditoria e politicas de acesso.
- IA Profissional/orquestrador com limites, logs e revisao humana.
- Investimentos e Dashboard do Clovis conectados ao admin.
- Portal do cliente e notificacoes sem vazamento de informacao.

## Como a proxima IA deve agir

Antes de mexer neste repertorio, ler este arquivo, verificar se a demanda exige backend e consultar as regras centrais em governanca/documentacao. Se a parte real ainda nao puder ser feita, deixar o proximo passo aqui em vez de criar uma promessa falsa no frontend.

© Jus 9 Tecnologia Juridica - software livre, autoria preservada.