# API de Autenticação e Permissões - FastAPI

Este projeto fornece uma API RESTful segura, desenvolvida com **FastAPI**, para gerenciar usuários, permissões e autenticação com **JWT**, além de recursos como **registro de logs de acesso** e **recuperação de senha**.

---

## 🚀 Tecnologias Utilizadas

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
