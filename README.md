**Atenção: O banco de dados está sendo criado a partir de um script em python, siga as instruções de instalação para adicionar.**

### Mural Virtual

Trabalho integrador da 4ª fase do curso de Sistemas de Informação da UNIPLAC (2019/2).

**Grupo**: Bruno Camargo, Elias, Érico. 

### Sumário

- [Instalação](#instalação)
- [Documentação](#documentação)
- [Tecnologias utilizadas](#tecnologias)

### Instalação

Clone o repositório

```
git clone https://github.com/bruno7kp/mural-virtual.git
```

No diretório raiz do projeto, execute os seguintes comandos para criar o ambiente virtual e instalar as bibliotecas utilizadas

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**IMPORTANTE:**

Copie o conteúdo do arquivo ```.env.example``` que está na raiz do projeto e cole dentro de um **novo** arquivo com o nome ```.env``` também na raiz.

Depois altere os valores dentro do arquivo ```.env``` com os dados de acesso ao banco de dados

Caso ainda não tenha criado, você pode criar o banco de dados através do comando abaixo, basta colocar um nome de banco válido em ```DB_NAME``` no arquivo ```.env```

```
python run.py create-database
```

Após o banco estar criado, execute o seguinte comando para criar as tabelas e adicionar usuários ao sistema

```
python run.py migrate-database
```

Os usuários cadastrados tem os seguintes dados de acesso:
```
Administrador
CPF/Login: 000.000.000-00
Senha: 123456
```
```
Moderador Notícias
CPF/Login: 111.111.111-11
Senha: 123456
```
```
Moderador Avisos
CPF/Login: 222.222.222-22
Senha: 123456
```
```
Usuário Padrão
CPF/Login: 333.333.333-33
Senha: 123456
```

Por fim, execute os comandos abaixo para rodar o projeto

```
set FLASK_ENV='development'
set FLASK_DEBUG=1
python -m flask run
```

### Documentação

- [Engenharia de Software](engenharia)
    - [Requisitos](engenharia/Requisitos.md)
    - [Histórias de usuários](engenharia/Histórias%20de%20usuário.md)
    - [Protótipo](https://xd.adobe.com/view/f1172239-6a23-42ff-67a1-1df87d96ea71-8726/)
    - [Diagrama do Banco de Dados](engenharia/Diagrama%20de%20banco%20de%20dados.png) - [(Online)](https://dbdiagram.io/d/5d8befd4ff5115114db4a296)
    - [Diagrama de Classes](engenharia/Diagrama%20de%20classes.pdf) - [(Online)](https://www.draw.io/#HBruno7kp%2Fmural-virtual%2Fmaster%2Fengenharia%2FDiagram%20de%20classes.drawio)
    - [Diagrama de Caso de Uso - Cadastro de anúncio pelo usuário padrão (nível 4)](engenharia/Diagrama%20de%20Caso%20de%20Uso%20-%20Cadastro%20de%20anúncio%20por%20usuário%20padrão.pdf)
    - [Diagrama de Caso de Uso - Gerenciamento de avisos, anúncios e notícias](engenharia/Diagrama%20%20de%20Caso%20de%20Uso%20-%20Gerenciamento%20de%20avisos,%20anúncios%20e%20notícias.pdf)

- [UX](ux)
    - [360 View](ux/360%20View.pptx)
    - [Cadastro](ux/Cadastro.jpeg)
    - [Home](ux/Home.jpeg)
    - [Avisos](ux/Avisos.jpeg)
    - [Noticias](ux/Noticias.jpeg)
    - [Jornada do usuário - Cadastro de notícias](ux/Jornada%20do%20usuário%20-%20Cadastro%20de%20notícias.xlsx)
    - [Jornada do usuário - Visualizar Anúncios](ux/Jornada%20do%20usuário%20-%20Visualizar%20Anúncios.xlsx)
    - [Jornada do usuário - Visualizar notícias](ux/Jornada%20do%20usuário%20-%20Visualizar%20notícias.xlsx)
    - [UI - Visual Design](ux/https://xd.adobe.com/view/f1172239-6a23-42ff-67a1-1df87d96ea71-8726/)
    - [Wireframes](ux/Wireframes.pdf)
    
    
### Tecnologias

**Banco de dados**


*MySQL (4.8.4)*: O MySQL é um sistema de gerenciamento de banco de dados, que utiliza a linguagem SQL como interface. É atualmente um dos sistemas de gerenciamento de bancos de dados mais populares da Oracle Corporation, com mais de 10 milhões de instalações pelo mundo.

---

**Backend**

*Python (3.7)*: Python é uma linguagem de programação de alto nível, interpretada, de script, imperativa, orientada a objetos, funcional, de tipagem dinâmica e forte.

**Bibliotecas**

*Flask (1.1.1)*: Flask é um pequeno framework web escrito em Python e baseado na biblioteca WSGI Werkzeug e na biblioteca de Jinja2.

*Jinja2 (2.10.1)*: O Jinja é um mecanismo de templates para a linguagem de programação Python.

*bcrypt (3.1.7)*: bcrypt é um método de criptografia do tipo hash para senhas.

*flask-paginate (0.5.5)*: Cria paginação em HTML para lista de anúncios, notícias e avisos.

*PyMySQL (0.9.3)*: Biblioteca para conectar ao banco de dados MySQL.

*python-dotenv (0.10.3)*: Utilizado para carregar informações dos arquivos '.env'.

---

**Frontend**


*HTML (5)*: HTML é uma linguagem de marcação utilizada na construção de páginas na web.

*CSS (3)*: Cascading Style Sheets é um mecanismo para adicionar estilo a um documento web.

*Javascript (ES6)*: JavaScript é uma linguagem de programação interpretada estruturada, de script em alto nível com tipagem dinâmica fraca e multi-paradigma.

*Bootstrap (4.1.3)*: Bootstrap é um framework web com código-fonte aberto para desenvolvimento de componentes de interface e front-end para sites e aplicações web usando HTML, CSS e JavaScript.

*FontAwesome (4.7.0)*: Conjunto de ícones para aplicações web.

*jQuery (3.4.1)*: jQuery é uma biblioteca de funções JavaScript que interage com o HTML, desenvolvida para simplificar os scripts interpretados no navegador do cliente.

*OwlCarousel (2.2.1)*: Plugin em jQuery que cria galerias de imagens (sliders).

*imaskjs (5.2.1)*: Biblioteca em JavaScript para criação de campos de texto com máscara.

*SB Admin 2 (4.0.7)*: Tema para a área administrativa baseada no Bootstrap.

*DataTables (1.10.19)*: Plugin em jQuery para a criação de tabelas interativas, com busca e páginação automatizadas.

*CKEditor (4)*: Plugin escrito em JavaScript para criação de textos formatados com estilos CSS e HTML.

*Sortable (1.10.1)*: Plugin em JavaScript utilizado para ordenar elementos HTML, como imagens, linhas de uma tabela, etc.

*SweetAlert 2 (9.4.0)*: Plugin em JavaScript para mostrar caixas de diálogo customizadas.
