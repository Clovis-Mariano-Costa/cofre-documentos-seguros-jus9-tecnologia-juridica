# Especificacao tecnica - Anexos, OCR e memoria curta v1.0

Data: 2026-06-04
Classificacao: INTERNO / TECNICO

## 1. Arquitetura sugerida

Fluxo ideal:

1. Frontend recebe anexo.
2. Frontend valida tipo, tamanho e aviso de seguranca.
3. Worker/backend cria registro temporario de upload.
4. Extrator tenta obter texto direto.
5. Se nao houver texto, OCR e acionado.
6. Classificador marca riscos e tipo documental.
7. Chat recebe pergunta atual + memoria curta + resumo do anexo.
8. Charlie Echo responde com links, acoes e limites.

## 2. Sem backend pago

Para MVP local/estatico, e possivel comecar com:

- upload apenas no navegador;
- leitura de `.txt`, `.md`, `.csv`;
- PDF textual com biblioteca JavaScript;
- imagem com OCR local opcional;
- memoria curta em `sessionStorage`;
- sem guardar arquivo em servidor.

Limitacao: OCR local pode ser pesado e menos confiavel.

## 3. Com worker/backend

Para producao, recomenda-se:

- endpoint `/api/anexos/upload`;
- endpoint `/api/anexos/extrair-texto`;
- endpoint `/api/anexos/ocr`;
- endpoint `/api/chat/contexto`;
- armazenamento temporario com expiracao;
- logs de auditoria;
- limite por usuario, sessao e tipo.

## 4. Modelo de estado da conversa

```json
{
  "sessionId": "demo-session",
  "module": "ia-profissional",
  "currentTopic": "analise de contrato",
  "lastUserIntent": "listar riscos",
  "activeFiles": [
    {
      "fileId": "temp-001",
      "name": "contrato.pdf",
      "type": "application/pdf",
      "textStatus": "extracted",
      "summary": "Contrato de prestacao de servicos com clausulas de prazo, pagamento e rescisao.",
      "safetyFlags": ["dados_pessoais_possiveis", "revisao_humana"]
    }
  ],
  "conversationSummary": "Usuario pediu resumo do contrato e agora quer riscos.",
  "openTasks": ["listar riscos", "sugerir checklist"],
  "answeredPoints": ["resumo inicial entregue"]
}
```

## 5. Prompt interno sugerido

Antes de responder, o motor da Charlie Echo deve receber:

```text
Voce e Charlie Echo no modulo {module}.
Use a pergunta atual, o resumo da conversa e os anexos ativos.
Se a pergunta atual for continuacao, preserve o assunto anterior.
Se o referente estiver ambiguo, pergunte confirmacao curta.
Nao invente leitura de anexo. Se OCR falhar, informe.
Classifique riscos de sigilo e recomende revisao humana quando necessario.
```

## 6. Politica de contexto

Ordem de prioridade:

1. instrucao de seguranca e governanca;
2. modulo/persona atual;
3. pergunta atual;
4. anexo ativo;
5. resumo da conversa;
6. historico recente;
7. links confiaveis externos.

## 7. Limites iniciais sugeridos

- Imagem: ate 10 MB no MVP.
- PDF: ate 20 MB no MVP.
- DOCX/XLSX: ate 15 MB no MVP.
- Maximo inicial: 5 anexos por conversa.
- Texto extraido: resumir quando passar do limite de contexto.

## 8. Auditoria

Registrar:

- data;
- modulo;
- tipo de arquivo;
- tamanho;
- se OCR foi usado;
- se houve alerta de sigilo;
- acao solicitada;
- se download foi gerado.

Nao registrar conteudo integral sensivel em logs publicos.
