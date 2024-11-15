-- Cria o banco de dados
CREATE DATABASE banco_curriculos;

-- Seleciona o banco de dados
USE banco_curriculos;

-- Cria a tabela alunos
CREATE TABLE alunos (
    id_aluno INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    telefone VARCHAR(50),
    nivel_ensino ENUM('Fundamental', 'Médio', 'Superior'),
    area_emprego VARCHAR(255)
);

-- Cria a tabela Matricula
CREATE TABLE Matricula (
    id_matricula INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT,
    status ENUM('Ativo', 'Inativo') NOT NULL,  -- Adicionando ENUM para status
    FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno)
);

-- Cria a tabela curriculos
CREATE TABLE curriculos (
    idcurriculos INT AUTO_INCREMENT PRIMARY KEY,
    caminho_arquivo VARCHAR(255) NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_aluno INT,
    FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno)
);
DESCRIBE Matricula;
ALTER TABLE alunos ADD COLUMN sobrenome VARCHAR(255);
ALTER TABLE curriculos 
ADD COLUMN arquivo BLOB;
ALTER TABLE curriculos MODIFY COLUMN arquivo LONGBLOB;
ALTER TABLE curriculos MODIFY COLUMN caminho_arquivo VARCHAR(255) DEFAULT '';



