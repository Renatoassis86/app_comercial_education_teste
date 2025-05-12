
-- Criar o banco de dados (executar apenas uma vez)
CREATE DATABASE comercialcve;
\c comercialcve  -- Conecta ao banco (no terminal PostgreSQL)

-- Criar tabela de escolas
DROP TABLE IF EXISTS escolas;

CREATE TABLE escolas (
    id SERIAL PRIMARY KEY,
    nome_escola VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100),
    cep VARCHAR(20),
    rua VARCHAR(255),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    complemento VARCHAR(255),
    numero VARCHAR(20),
    contato_nome VARCHAR(100),
    contato_cargo VARCHAR(50),
    perfil_pedagogico VARCHAR(100),
    origem_lead VARCHAR(100),
    responsavel_pedagogico VARCHAR(100),
    escola_paideia VARCHAR(10),
    cnpj VARCHAR(20),
    diretor_nome VARCHAR(100),
    qtd_infantil INT DEFAULT 0,
    qtd_fund1 INT DEFAULT 0,
    qtd_fund2 INT DEFAULT 0,
    qtd_medio INT DEFAULT 0,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela de registros (com chave estrangeira corrigida)
DROP TABLE IF EXISTS registros;

CREATE TABLE registros (
    id SERIAL PRIMARY KEY,
    id_escola INT REFERENCES escolas(id) ON DELETE CASCADE,
    data_contato DATE NOT NULL,
    resumo TEXT,
    meio_contato VARCHAR(100),
    interesse VARCHAR(50),
    prontidao VARCHAR(50),
    abertura VARCHAR(50),
    encaminhamento VARCHAR(100),
    responsavel VARCHAR(100),
    contato VARCHAR(100),
    cargo VARCHAR(50),
    qtd_infantil INT,
    qtd_fund1 INT,
    qtd_fund2 INT,
    qtd_medio INT,
    potencial_financeiro NUMERIC(10, 2),
    classificacao_lead VARCHAR(50),
    probabilidade INT,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
