- UNIPLAC
- Sistemas de Informação – 4º Semestre
- Engenharia de Software
- Bruno, Elias, Érico.

### Projeto Integrador - Mural Virtual UNIPLAC
#### Histórias de usuário

------

Como Administrador, preciso gerenciar o cabeçalho da universidade no site, podendo alterar o nome, telefone e e-mail.

**Critérios de aceite:**

- [ ] Os dados do cabeçalho só podem ser alterados dentro da área administrativa.
- [ ] Apenas usuários de nível mais alto (nível 1) podem alterar os dados do cabeçalho.

------

Como Administrador, preciso gerenciar as imagens que ficarão em destaque na página inicial. As imagens precisam aparecer uma de cada vez, sendo alteradas conforme passe o tempo. Preciso também que algumas imagens possam redirecionar o usuário para alguma parte do site ou para sites externos quando clicada.

**Critérios de aceite:**

- [ ] As imagens da página inicial só podem ser alteradas dentro da área administrativa.
- [ ] Apenas usuários de nível mais alto (nível 1) podem alterar as imagens.
- [ ] O usuário pode informar um link para a imagem, que irá redirecionar ao fazer o clique na mesma.

------

Como Administrador (nível 1), ou como usuário de nível 3, deve ser possível gerenciar avisos, com título, descrição, e período de publicação (período que ficará disponível ao público no sistema).

**Critérios de aceite:**

- [ ] Os avisos só podem ser gerenciados pela área administrativa.
- [ ] Apenas usuários de nível 1 ou de nível 3 podem gerenciar os avisos.

------

Como Administrador (nível 1), ou como usuário de nível 2, deve ser possível gerenciar notícias, com título, conteúdo, imagens, e período de publicação (período que ficará disponível ao público no sistema).

**Critérios de aceite:**

- [ ] As notícias só podem ser gerenciados pela área administrativa.
- [ ] Apenas usuários de nível 1 ou de nível 2 podem gerenciar as notícias.
- [ ] Pode ser cadastrado uma galeria de fotos relacionadas a notícia.

-----

Como usuário de qualquer nível, deve ser possível gerenciar seus próprios anúncios, com título, conteúdo, imagens, e período de publicação (período que ficará disponível ao público no sistema). Como usuário de nível 1, 2 ou 3, deve ser possível alterar anúncios de outros usuários também. Como usuário de nível 4, o anúncio deve passar por uma triagem, onde usuários de nível superior devem aprovar para que esses anúncios tenham visibilidade na área pública do site.

**Critérios de aceite:**

- [ ] As notícias só podem ser gerenciados pela área administrativa.
- [ ] Usuários de todos os níveis podem cadastrar anúncios.
- [ ] Pode ser cadastrado uma galeria de fotos relacionadas ao anúncio.
- [ ] Usuários de nível 4 só podem alterar seus próprios anúncios.
- [ ] Usuários de nível 4 só podem editar anúncios aprovados na triagem.
- [ ] Usuários de nível 1, 2 e 3, podem adicionar anúncios sem necessidade de triagem.
- [ ] Usuários de nível 1, 2, e 3, podem aprovar anúncios de usuários de nível 4.
- [ ] Na área administrativa, deve haver uma área de anúncios aguardando aprovação.

------

Por motivos de auditoria, será necessário que todas ações realizadas na área administrativa sejam armazenadas e que o usuário de nível 1 possa visualizá-las, podendo filtrar as ações.

**Critérios de aceite:**

- [ ] Todas as ações dentro da área administrativa devem gerar log contendo:
- [ ] Usuário
- [ ] Ação realizada
- [ ] Data e hora
- [ ] Apenas usuários de nível 1 podem acessar os logs.
- [ ] Deverá ter filtro por data, ação, e usuário.
- [ ] Deve haver um local para mostrar todos logs, bem como, poder visualizar logs apenas relacionadas a uma entidade específica, ex: logs de alteração de uma notícia, de um anúncio, etc.

------

Deve ser possível realizar cadastro de usuários pela área pública do sistema. Os usuários devem ter o nível de permissão mais baixo (nível 4).
Como administrador (nível 1) deve ser possível alterar os dados do usuário, incluindo o nível de acesso do mesmo.

**Critérios de aceite:**

- [ ] A área pública do sistema deve ter um formulário para cadastro do usuário, com os dados de:
- [ ] Nome
- [ ] E-mail
- [ ] Senha
- [ ] Na área administrativa, apenas usuários do nível 1, podem editar o cadastro de outros usuários, e o nível do mesmo.

------

O acesso aos anúncios, notícias e avisos deve ser público, aparecendo apenas durante o período de publicação. Eles são mostrados de forma resumida na página inicial do sistema, e podem ser abertos em uma página com as informações completas.

**Critérios de aceite:**

- [ ] A página inicial do sistema devem mostrar os anúncios, notícias e avisos de forma resumida.
- [ ] Deve haver uma página com a listagem (paginada) de todas as notícias, outra para os anúncios e outra para os avisos, também de forma resumida.
- [ ] Deve haver uma página para mostrar as informações completas dos anúncios, avisos e notícias.
