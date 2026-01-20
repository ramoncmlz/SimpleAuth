## 📌 Sobre o projeto

Este projeto é um **sistema de login em Python executado no terminal**, desenvolvido com foco em aprendizado de lógica de programação, autenticação e controle de usuários.

O sistema permite registro, login e gerenciamento de contas, com diferenciação entre usuários comuns e administrador.
Os dados dos usuários são armazenados em um **arquivo de texto (`.txt`)**, simulando persistência de dados sem uso de banco de dados, com validações de segurança e controle de tentativas de acesso.

---

- Ao iniciar o programa:
  - Os dados do arquivo são lidos
  - Cada linha é convertida em um **dicionário Python**
  - Os usuários são carregados em memória

- Ao sair do sistema:
  - Os dicionários são convertidos novamente em texto
  - O arquivo é sobrescrito com os dados atualizados

Esse processo foi implementado **com auxílio de IA**, com o objetivo de **aprender como estruturar, converter e persistir dados entre arquivos de texto e estruturas Python**.

---

## 🔐 Regras de segurança

- Username:
  - Deve ser todo em letras minúsculas
  - Não pode ser duplicado

- Senha:
  - Mínimo de 8 caracteres
  - Deve começar com letra maiúscula
  - Deve conter pelo menos um número

- Login:
  - 3 tentativas inválidas
  - Bloqueio temporário de 3 minutos após exceder o limite

---

## 🎯 Objetivo do projeto

Este projeto foi criado para **treinar conceitos fundamentais de backend**, como:

- lógica de autenticação
- controle de estado
- manipulação de arquivos
- listas e dicionários
- validações
- simulação de segurança básica

É um projeto educacional, mas já estruturado pensando em evolução real.

---

## 🚧 Próximos passos

- 🚀 Utilizar o framework **FastAPI** para conectar o sistema a um banco de dados
- 🗄️ Armazenar os dados de usuários em um banco **SQLite**
- 🔒 Implementar **criptografia de senha**
- 🧪 Melhorar validações, tratamento de erros e organização do código

---

## ▶️ Como executar

```bash
python main.py

