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

Copie o conteúdo do arquivo ```.env.example``` e cole dentro de um arquivo ```.env```

Depois altere os valores dentro do arquivo ```.env``` para configurar o acesso ao banco de dados

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