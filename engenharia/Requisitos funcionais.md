
UNIPLAC

Sistemas de Informação – 4º Semestre

Engenharia de Software

Bruno, Elias, Érico.


### Projeto Integrador - Mural Virtual UNIPLAC


#### Requisitos de usuário


<table>
  <tr>
   <td>Código
   </td>
   <td>Descrição
   </td>
   <td>Prioridade
   </td>
  </tr>
  <tr>
   <td>RF 1
   </td>
   <td>Manter cadastro de usuário do Mural Virtual
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 1.1
   </td>
   <td>Usuários podem ser cadastrados através da área administrativa, ou podem se cadastrar pelo área pública
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 1.2
   </td>
   <td>Os dados de cadastro do usuário devem ser:
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 1.2.1
   </td>
   <td>Nome, e-mail, telefone, CPF, e nível de usuário
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RNF 1.3
   </td>
   <td>Deve haver 4 níveis de usuário, sendo 4 o mais baixo e o 1 mais alto (com mais permissões)
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RNF 1.3.1
   </td>
   <td>Ao se cadastrar no sistema, o usuário por padrão terá o nível de permissão mais baixo (nível 4)
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RNF 1.3.2
   </td>
   <td>Apenas usuários de nível mais alto (nível 1) podem cadastrar usuários escolhendo um nível, bem como alterar o nível de outros usuários
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 2
   </td>
   <td>Gerenciar cabeçalho com dados da universidade
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 2.1
   </td>
   <td>Os dados do cabeçalho devem ser:
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 2.1.1
   </td>
   <td>Nome, telefone, e-mail e 10 imagens
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RNF 2.2
   </td>
   <td>Apenas usuários de nível mais alto (nível 1) podem gerenciar os dados do cabeçalho pela área administrativa
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 2.3
   </td>
   <td>Os dados devem ser mostrados na área pública (não necessita autenticação) do Mural Virtual
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RNF 2.3.1
   </td>
   <td>As imagens cadastradas devem ser mostradas e trocadas dinamicamente na página inicial do Mural Virtual
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 3
   </td>
   <td>Manter cadastro de avisos do Mural Virtual
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 3.1
   </td>
   <td>Os dados do aviso devem ser:
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 3.1.1
   </td>
   <td>Título, descrição, data e hora de entrada e saída do ar
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RNF 3.2
   </td>
   <td>Apenas usuários do nível 1 ou do nível 3 podem gerenciar os avisos pela área administrativa
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 3.3
   </td>
   <td>Os avisos que devem aparecer na área pública do Mural Virtual são aqueles que ainda estão ativos, ou seja, dentro do período de publicação selecionado
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 4
   </td>
   <td>Manter cadastro de notícias do Mural Virtual
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 4.1
   </td>
   <td>Os dados da notícia devem ser:
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 4.1.1
   </td>
   <td>Título, conteúdo, imagens, data e hora de entrada e saída do ar
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RNF 4.2
   </td>
   <td>Apenas usuários do nível 2 ou do nível 1 podem gerenciar as notícias
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 4.3
   </td>
   <td>As notícias que devem aparecer na área pública do Mural Virtual são aquelas que ainda estão ativas, ou seja, dentro do período de publicação selecionado
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 4.3.1
   </td>
   <td>A notícia deve ter uma página exclusiva para leitura completa, que será acessível ao clicar na notícia, na página inicial
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 5
   </td>
   <td>Manter cadastro de anúncios do Mural Virtual
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 5.1
   </td>
   <td>Os dados do anúncio devem ser:
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 5.1.1
   </td>
   <td>Título, conteúdo, imagens, data e hora de entrada e saída do ar
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RNF 5.2
   </td>
   <td>O cadastro de anúncios pode ser realizado por usuários de qualquer nível, dentro da área administrativa. E devem passar por aprovação, antes de serem mostrados na área pública do Mural Virtual
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RNF 5.2.1
   </td>
   <td>Se for um usuário nível 4, o cadastro deve ficar em uma “Fila de Moderação”, devendo ser liberado ou negado através da área administrativa por qualquer usuário dos níveis 1, 2 ou 3
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RNF 5.2.2
   </td>
   <td>Usuários de nível 1, 2 ou 3 terão seus anúncios automaticamente liberado
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RNF 5.2.3
   </td>
   <td>Usuários com nível 4 podem editar somente seus próprios anúncios, e somente enquanto eles ainda estiverem pendentes de aprovação
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 5.3
   </td>
   <td>Os anúncios que devem aparecer na área pública do Mural Virtual são aqueles que ainda estão ativos, ou seja, dentro do período de publicação selecionado
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 5.3.1
   </td>
   <td>O anúncio deve ter uma página exclusiva para leitura completa, que será acessível ao clicar na notícia, na página inicial
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 6
   </td>
   <td>Deve ser armazenado um histórico das informações de todas as ações realizadas na área administrativa
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 6.1
   </td>
   <td>As seguintes informações devem estar presentes no histórico:
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 6.1.1
   </td>
   <td>A ação realizada, data, hora e quem realizou (usuário)
   </td>
   <td>Obrigatório
   </td>
  </tr>
</table>



## Requisitos de sistema


<table>
  <tr>
   <td>Código
   </td>
   <td>Descrição
   </td>
   <td>Prioridade
   </td>
  </tr>
  <tr>
   <td>RF 1
   </td>
   <td>O Mural Virtual deve estar disponível nas seguintes plataformas:
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 1.1
   </td>
   <td>Totens que serão instalados em pontos chave da universidade, smartphones, microcomputadores e similares
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 2
   </td>
   <td>O sistema será disponibilizado pela WEB
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 2.1
   </td>
   <td>Para o desenvolvimento do sistema, serão utilizadas tecnologias para WEB:
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 2.1.1
   </td>
   <td>HTML, CSS e JavaScript para a parte visual e de interação do sistema
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 2.1.2
   </td>
   <td>Python, com o framework Flask, para o lado do servidor
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 2.2
   </td>
   <td>Para atender as diversas plataformas, o sistema deverá ser responsivo (adaptável ao tamanho da tela do dispositivo)
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 3
   </td>
   <td>Todos os dados mantidos no sistema devem ser salvos em um banco de dados
   </td>
   <td>Obrigatório
   </td>
  </tr>
  <tr>
   <td>RF 3.1
   </td>
   <td>Isso inclui imagens que também devem salvas em banco de dados
   </td>
   <td>Obrigatório
   </td>
  </tr>
</table>
