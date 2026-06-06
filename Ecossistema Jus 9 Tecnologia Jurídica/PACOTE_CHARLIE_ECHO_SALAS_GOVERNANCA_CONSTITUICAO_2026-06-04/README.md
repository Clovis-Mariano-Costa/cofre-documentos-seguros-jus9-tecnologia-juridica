# Pacote Charlie Echo - Salas, governanca e constituicao

Data: 2026-06-04
Classificacao: INTERNO / GOVERNANCA / IDENTIDADE / OPERACIONAL
Responsavel tecnico: Charlie Fox da Costa / Codex
Revisao humana: obrigatoria antes de publicacao, deploy ou uso com dados reais

## Objetivo

Este pacote organiza a proxima camada da Charlie Echo:

- salas de chat por modulo, como conversas separadas;
- memoria curta por sala;
- aparencia padrao com personalidade por ambiente;
- atualizacao de governanca;
- constituicao operacional;
- leis internas;
- protocolos praticos;
- prioridade de evolucao para MVPs.

## Arquivos do pacote

1. `CONSTITUICAO_CHARLIE_ECHO_v1_0.md`
   - principios, identidade, limites, liberdade criativa e deveres.

2. `LEIS_CHARLIE_ECHO_v1_0.md`
   - leis internas para memoria, anexos, salas, links, sigilo e revisao humana.

3. `PROTOCOLOS_SALAS_DE_CHAT_CHARLIE_ECHO_v1_0.md`
   - funcionamento de salas, historico, contexto, anexos e encerramento.

4. `PADRAO_VISUAL_E_PERSONALIDADE_POR_MODULO_v1_0.md`
   - aparencia comum e variacoes por ambiente.

5. `PRIORIDADES_OPERACIONAIS_CHARLIE_ECHO_v1_0.md`
   - ordem pratica de execucao para os MVPs e modulos da Charlie.

6. `MODELO_SALA_CHAT_CHARLIE_ECHO_v1_0.json`
   - modelo de dados inicial para sala/conversa.

## Decisao central

Charlie Echo deve poder ter muitas salas de conversa, mas cada sala deve ser governada.

Uma sala deve conter:

- assunto;
- modulo;
- personalidade ativa;
- resumo da conversa;
- anexos ativos;
- tarefas abertas;
- alertas de sigilo;
- historico da sessao;
- links e downloads gerados.

## Regra visual

Todos os modulos devem compartilhar a mesma arquitetura de chat, para que o usuario reconheca a Charlie Echo em qualquer lugar.

Cada modulo pode variar tom, cores secundarias, acoes rapidas e linguagem, para preservar personalidade propria.

## Relacao com pacote anterior

Este pacote complementa:

`PACOTE_CHARLIE_ECHO_ANEXOS_OCR_MEMORIA_2026-06-04`

O pacote anterior ensina anexos, OCR e memoria curta. Este pacote organiza onde essa memoria vive: nas salas de chat.
