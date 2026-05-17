# Orientações para backend futuro

CLASSIFICAÇÃO: PÚBLICO / TÉCNICO / NÃO INSERIR SEGREDOS

Este repertório pode conter protótipos visuais e documentação. Produção real deverá depender de backend seguro.

## Arquitetura sugerida

1. Front-end estático em Cloudflare Pages ou GitHub Pages.
2. API segura em Cloudflare Workers ou backend equivalente.
3. Secrets em Cloudflare Workers Secrets / Secrets Store / GitHub Secrets.
4. Banco de dados com controle de acesso.
5. Senhas com hash forte, preferencialmente Argon2id ou bcrypt com custo adequado.
6. Sessões/tokens com expiração, rotação e escopo.
7. Logs de acesso e auditoria em repertório/sistema próprio.
8. Armazenamento privado para documentos, por exemplo R2 privado ou equivalente.
9. Separação por perfil: advogado/defensor, professor, mestre, doutor, estudante, grupo, equipe, admin.
10. Revisão humana antes de produção.

## Para o MVP atual

O MVP visual é demonstrativo. Nenhum dado real deve ser usado.

© Jus 9 Tecnologia Jurídica — software livre, autoria preservada.
