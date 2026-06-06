# Protocolos de salas de chat da Charlie Echo v1.0

Data: 2026-06-04
Classificacao: INTERNO / PROTOCOLO / CHAT

## 1. Conceito

Sala de chat e o container de uma conversa.

Ela guarda o contexto local daquela conversa, sem misturar assuntos de outras salas.

## 2. Componentes da sala

Cada sala deve conter:

- identificador;
- titulo;
- modulo;
- personalidade ativa;
- data de criacao;
- data da ultima mensagem;
- resumo da conversa;
- mensagens;
- anexos ativos;
- links oferecidos;
- downloads gerados;
- tarefas abertas;
- alertas de seguranca.

## 3. Criacao de sala

Uma sala deve ser criada quando:

- o usuario clicar em "Nova conversa";
- o assunto mudar de forma relevante;
- o modulo mudar;
- houver novo dossie, aula, documento ou atendimento;
- o usuario pedir para separar o tema.

## 4. Continuidade dentro da sala

Antes de responder, Charlie deve verificar:

- pergunta atual;
- ultima pergunta do usuario;
- ultima resposta da Charlie;
- anexos ativos;
- resumo da sala;
- tarefas abertas.

Se a pergunta for continuidade, ela deve responder usando o contexto.

## 5. Ambiguidade

Se houver ambiguidade, Charlie deve perguntar:

"Voce quer que eu continue a analise da sala atual ou deseja abrir um novo assunto?"

## 6. Titulo automatico

Charlie pode sugerir titulo da sala:

- "Analise do contrato de servicos";
- "Aula sobre responsabilidade social";
- "Checklist do MVP Advogar";
- "Duvidas sobre investimento";
- "OCR de documento escaneado".

## 7. Resumo automatico

A cada bloco de conversa, Charlie deve atualizar resumo curto:

- objetivo;
- conclusoes;
- pendencias;
- anexos analisados;
- riscos;
- proximos passos.

## 8. Encerramento

Ao encerrar uma sala, Charlie pode oferecer:

- resumo final;
- checklist;
- arquivo para download;
- links usados;
- pendencias para revisao humana.

## 9. Salas por modulo

Todos os modulos podem ter salas:

- IA Profissional;
- IA Publica;
- Jus9 Verde;
- Universidade do Futuro;
- Aulas Charlie Echo;
- MVP Advogar;
- MVP Professor;
- MVP Estudante;
- MVP Empresa;
- MVP Investidor;
- demais MVPs.

## 10. Regras de seguranca

Sala de demo nao deve armazenar dados reais.

Sala profissional real deve exigir autenticacao, permissao, logs e politica de retencao.
