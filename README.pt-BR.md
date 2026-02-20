🇧🇷 Português | 🇺🇸 [English](README.md)

## 📌 Sobre o SimpleAuth

SimpleAuth é uma **API de autenticação de usuários desenvolvida com FastAPI**.

O projeto evoluiu de um sistema de login em terminal para um backend HTTP com persistência real, autenticação por token e controle de acesso.

---

## ⚙️ Funcionalidades

- Registro de usuário (`POST /register`)
- Login com token JWT (`POST /login`)
- Controle automático de tentativas inválidas
- Bloqueio temporário após múltiplas tentativas inválidas
- Logout por token (`POST /logout`)
- Alteração de username com invalidação automática da sessão (`POST /change-username`)
- Alteração de senha (`POST /change-password`)
- Exclusão de usuário somente por admin (`DELETE /delete-user`)
- Listagem de usuários somente por admin (`GET /show-users`)
- Verificação de autenticação (`GET /me`)

---

## 🧠 Como Funciona

- A API usa **SQLite** para persistência (`app/storage/simpleauth.db`).
- Senhas são armazenadas como **hash** (`pbkdf2_sha256` com `passlib`).
- A autenticação usa **JWT Bearer token**.
- O sistema garante uma sessão ativa por usuário com:
  - `session_active`
  - `session_version`
- Endpoints protegidos identificam o usuário atual através do token.

---

## 🆕 O Que Há De Novo Em Relação À Versão Anterior

- Migração de usuários em memória para **persistência em SQLite**
- Substituição de estado `is_logged` por **autenticação com JWT**
- Inclusão de **hash de senha**
- Invalidação automática de sessão após troca de username
- Padronização de erros HTTP (`400`, `401`, `403`, `404`, `409`, `429`)
- Fluxos de requisição testados com Postman

---

## ▶️ Como Executar

```bash
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

A documentação da API é gerada automaticamente pelo Swagger.
