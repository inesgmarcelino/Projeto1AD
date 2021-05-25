-- Aplicações distribuídas - Projeto 4 - listagem1.sql
-- Grupo: 25
-- Números de aluno: Sofia Lourenço 54950, Inês Marcelino 54991

PRAGMA foreign_keys = ON;
CREATE TABLE utilizadores (
  id INTEGER PRIMARY KEY,
  nome TEXT,
  senha TEXT
);
CREATE TABLE artistas (
  id INTEGER PRIMARY KEY,
  id_spotify TEXT,
  nome TEXT
);
CREATE TABLE albuns (
  id INTEGER PRIMARY KEY,
  id_spotify TEXT,
  nome TEXT,
  id_artista INTEGER,
  FOREIGN KEY (id_artista) REFERENCES artistas(id)
);
CREATE TABLE avaliacoes (
  id INTEGER PRIMARY KEY,
  sigla TEXT,
  designacao TEXT
);
CREATE TABLE listas_albuns (
  id_user INTEGER,
  id_album INTEGER,
  id_avaliacao INTEGER,
  PRIMARY KEY (id_user, id_album),
  FOREIGN KEY (id_user) REFERENCES utilizadores(id),
  FOREIGN KEY (id_album) REFERENCES albuns(id),
  FOREIGN KEY (id_avaliacao) REFERENCES avaliacoes(id)
);