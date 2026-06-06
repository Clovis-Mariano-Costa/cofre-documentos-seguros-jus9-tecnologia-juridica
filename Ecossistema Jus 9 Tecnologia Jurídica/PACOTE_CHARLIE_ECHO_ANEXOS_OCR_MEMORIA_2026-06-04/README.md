# Pacote Charlie Echo - Anexos, OCR e memoria conversacional

Data: 2026-06-04
Classificacao: INTERNO / OPERACIONAL / GOVERNANCA
Responsavel tecnico: Charlie Fox da Costa / Codex
Revisao humana: obrigatoria antes de publicacao, deploy ou uso com dados reais

## Objetivo

Preparar a Charlie Echo para:

- aceitar mais tipos de anexo;
- fazer leitura OCR de imagens e PDFs escaneados;
- analisar documentos com governanca juridica;
- concatenar perguntas dentro da mesma conversa;
- lembrar o contexto imediato sem criar memoria permanente indevida;
- operar em todos os modulos e MVPs com personalidade adequada ao ambiente.

## Arquivos do pacote

1. `PROTOCOLO_ANEXOS_OCR_MEMORIA_CHARLIE_ECHO_v1_0.md`
   - regra de comportamento, seguranca, anexos, OCR e continuidade de conversa.

2. `ESPECIFICACAO_TECNICA_ANEXOS_OCR_MEMORIA_v1_0.md`
   - arquitetura tecnica sugerida para frontend, worker/backend, extracao, OCR e memoria curta.

3. `CHECKLIST_IMPLEMENTACAO_MODULOS_CHARLIE_ECHO_v1_0.md`
   - lista pratica para replicar nos modulos da Charlie Echo e nos MVPs.

4. `CONFIG_TIPOS_ANEXO_E_ACOES_CHARLIE_ECHO_v1_0.json`
   - configuracao inicial de tipos aceitos, acoes sugeridas e limites.

## Decisao principal

A Charlie Echo deve ter dois tipos de memoria:

- memoria curta de sessao: conversa atual, perguntas anteriores, anexos citados e objetivo do usuario;
- memoria resumida governada: resumo tecnico da conversa, apenas quando permitido e sem guardar dados sigilosos em ambiente demonstrativo.

Ela nao deve usar memoria permanente irrestrita em MVP publico.

## Ordem de implementacao sugerida

1. Implementar memoria curta no chat da IA Profissional.
2. Adicionar painel de anexos aceitos e aviso de seguranca.
3. Aceitar texto, PDF textual e imagens simples.
4. Adicionar OCR para imagem e PDF escaneado.
5. Criar acoes guiadas: resumir, extrair prazos, listar riscos, explicar, traduzir e gerar checklist.
6. Replicar para IA publica, IA social, aulas e demais MVPs.
7. Registrar auditoria e limites por modulo.

## Observacao

Este pacote e preparatorio. A implementacao real pode comecar local e gratuita, mas OCR e leitura de anexos em producao ficam melhores com worker/backend dedicado, limites de tamanho, logs e revisao humana.
