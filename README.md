### Mural Virtual

Trabalho integrador da 4ª fase do curso de Sistemas de Informação da UNIPLAC (2019/2).

**Grupo**: Bruno Camargo, Elias, Érico. 

### Sumário

- [Instalação](#instalação)
- [Documentação](#documentação)

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

Copie o conteúdo do arquivo ```.env.example``` e cole dentro de um novo arquivo ```.env```

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
    - [Requisitos funcionais](engenharia/Requisitos%20funcionais.md)
    - [Histórias de usuários](engenharia/Histórias%20de%20usuário.md)
    - [Protótipos](https://xd.adobe.com/view/f1172239-6a23-42ff-67a1-1df87d96ea71-8726/)
    - [Diagrama do Banco de Dados](https://dbdiagram.io/d/5d8befd4ff5115114db4a296)