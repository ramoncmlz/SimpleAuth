🇧🇷 Português | 🇺🇸 [Inglês](README.md)

📌 Sobre o projeto

Este projeto é um sistema de login simples em Python que roda no terminal.

A ideia era simular um fluxo básico de autenticação, com usuários convidados, usuários logados e um usuário administrador, cada um com diferentes opções de menu.

Tudo é feito usando apenas lógica e estruturas básicas do Python, sem banco de dados ou bibliotecas externas.

⚙️ O que você pode fazer

📝 Criar novos usuários

🔐 Fazer login usando nome de usuário e senha

🚪 Sair

📋 Navegar por um menu interativo no terminal

🛡️ Fazer login como administrador e gerenciar usuários

❌ Excluir usuários (com proteção para impedir a exclusão do administrador)

🧠 Como funciona nos bastidores

Os usuários são armazenados em uma lista de dicionário contendo nome de usuário e senha. O programa controla quem está logado através da variável `current_user`.

Com base nisso, ele decide qual menu exibir:

👤 Nenhum usuário logado → menu de convidado

👥 Usuário comum → menu padrão

🛡️ Administrador → menu com permissões extras

Um loop principal mantém o sistema em execução até que o usuário opte por sair.

🎯 Objetivo do Projeto

Criei este projeto para praticar lógica de programação em Python, principalmente:

- funções

- listas e dicionários

- estruturas condicionais

- loops

- fluxo do programa e controle de estado

É um projeto simples, mas ajuda muito a entender como os sistemas de login funcionam internamente.

🚧 Próximos passos (em desenvolvimento)

🔑 Opção para alterar a senha do usuário, como parte da evolução do sistema.

🔒 Implemente um sistema de segurança para limitar tentativas de login inválidas

📂 Armazene usuários em um arquivo .txt, permitindo salvar e carregar usuários registrados

🧪 Melhore as validações e a organização do código

▶️ Como executar

Basta executar o arquivo no terminal:

python user-menu.py
