DROP TABLE IF EXISTS tb_usuario CASCADE;
CREATE TABLE tb_usuario (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    nascimento DATE NOT NULL
);

DROP TABLE IF EXISTS tb_categoria CASCADE;
CREATE TABLE tb_categoria (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL
);

DROP TABLE IF EXISTS tb_setor CASCADE;
CREATE TABLE tb_setor (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL
);

DROP TABLE IF EXISTS tb_produto CASCADE;
CREATE TABLE tb_produto (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    categoria_id INTEGER NOT NULL,
    setor_id INTEGER NOT NULL,
    foreign key (categoria_id) references tb_categoria(id),
    foreign key (setor_id) references tb_setor(id)
);

insert into tb_usuario(nome, nascimento) values ('Administrador', '2024-07-23');