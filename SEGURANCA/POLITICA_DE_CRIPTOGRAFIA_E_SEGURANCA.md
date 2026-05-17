# Política de criptografia e segurança — orientação comum

CLASSIFICAÇÃO: PÚBLICO / SEGURANÇA / NÃO PUBLICAR SEGREDOS

## Princípio

Criptografia deve proteger dados reais; aviso visual não substitui segurança técnica.

## No GitHub

O GitHub deve conter apenas código, documentação, exemplos, `.env.example` e dados fictícios.

Nunca publicar:

- senhas reais;
- tokens;
- chaves privadas;
- seeds;
- `.env` real;
- dados pessoais sensíveis;
- documentos de clientes/usuários;
- documentos sigilosos de terceiros.

## Produção futura

- HTTPS obrigatório.
- Senhas com hash forte.
- Secrets fora do repositório.
- Controle de acesso por perfil.
- Logs de auditoria.
- Armazenamento privado para anexos.
- Revisão humana e governança.

© Jus 9 Tecnologia Jurídica — software livre, autoria preservada.
