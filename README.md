# API de Autenticação e Permissões - FastAPI

Este projeto fornece uma API RESTful segura, desenvolvida com **FastAPI**, para gerenciar usuários, permissões e autenticação com **JWT**, além de recursos como **registro de logs de acesso** e **recuperação de senha**.

---

## Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [SQLite3](https://www.sqlite.org/) (ou substituível por PostgreSQL, MySQL)
- [JWT (via python-jose)](https://github.com/mpdavis/python-jose)
- [Bcrypt (via Passlib)](https://passlib.readthedocs.io/)

---

##  Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio

# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt
```

## Executando o Projeto

```bash
# Inicie o servidor com Uvicorn
uvicorn app.main:app --reload
Acesse a documentação interativa em: http://localhost:8000/docs
```

## Funcionalidades

- Cadastro e autenticação de usuários (JWT)

- Controle de permissões (RBAC)

- Registro de logs de login, falhas e ações

- Recuperação e redefinição segura de senha

- Exclusão de contas conforme LGPD

- Ponto de integração com frontend via CORS

## Estrutura de Diretórios

```bash
app/
├── models/               # Modelos SQLAlchemy
├── routes/               # Rotas da API
├── schemas/              # Schemas (Pydantic)
├── utils/                # Funções auxiliares (hash, token)
├── database.py           # Conexão e configuração do banco
└── main.py               # Ponto de entrada da API
```

## Requisitos
Python 3.10+

Git

pip (gerenciador de pacotes do Python)

## Contato
Caso tenha dúvidas ou sugestões, sinta-se à vontade para abrir uma issue ou enviar um pull request!
