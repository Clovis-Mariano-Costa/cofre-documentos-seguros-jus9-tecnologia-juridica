# POLÍTICA DE CRIPTOGRAFIA E SEGURANÇA

## Regra geral

Nenhum segredo real deve ser publicado no GitHub.

Não versionar:

- senhas reais;
- tokens;
- chaves privadas;
- `.env` real;
- dados sensíveis;
- documentos de cliente;
- conteúdo secreto ou de cofre.

## Camadas recomendadas

1. GitHub público apenas com modelos, documentação e exemplos sem segredo real.
2. Cloudflare Access / Zero Trust para proteger rotas e áreas privadas.
3. Workers Secrets para chaves e tokens.
4. R2 privado para documentos protegidos.
5. URLs assinadas e temporárias para downloads sensíveis.
6. Logs mínimos de acesso e revisão humana.
7. Criptografia client-side para material de máxima sensibilidade, quando a chave puder ser guardada com segurança humana.

## Limite máximo prudente

O limite máximo recomendado é: autenticação forte + autorização por perfil + armazenamento privado + criptografia em repouso + criptografia em trânsito + secrets fora do GitHub + logs + revisão humana.

Para conteúdo realmente secreto, usar criptografia antes do upload e aceitar que a perda da chave pode significar perda definitiva do conteúdo.
