# Gerenciamento de Currículos
Este é um aplicativo de gerenciamento de currículos que permite o cadastro, atualização, remoção e busca de currículos em um banco de dados MySQL. O sistema também permite o upload de arquivos de currículo em formato PDF e sua vinculação aos alunos cadastrados.

# Funcionalidades
  Cadastro de Alunos: Permite cadastrar um novo aluno com informações como nome, e-mail, telefone, nível de ensino e área de emprego.
  
  Upload de Currículo: Após o cadastro de um aluno, é possível fazer o upload de seu currículo em formato PDF, que será armazenado diretamente no banco de dados como um campo BLOB.
  
  Edição de Cadastro: Permite editar as informações de um aluno, incluindo a possibilidade de atualizar seu currículo.
  
  Remoção de Aluno: Permite remover o cadastro de um aluno, incluindo seu currículo.
  
  Busca de Currículos: Permite buscar alunos e currículos por nome ou área de emprego.
  
  Exibição dos Últimos Cadastrados: Exibe uma lista dos últimos 10 alunos cadastrados, com a possibilidade de visualizar seus currículos.
  
  Abrir Currículo: Permite abrir o currículo em formato PDF diretamente do banco de dados.

  
# Banco de Dados
  O sistema utiliza o banco de dados MySQL para armazenar as informações dos alunos e seus currículos. Abaixo estão as tabelas utilizadas:
  
  alunos: Armazena as informações básicas do aluno.
  
  matricula: Armazena o status de matrícula do aluno.
  
  curriculos: Armazena os arquivos de currículo dos alunos em formato BLOB.
