from flask import Flask, request, jsonify, g

from helpers.database.__init_db import get_db_connection
from helpers.logging import logger

app = Flask(__name__)

# Padronizando requests para endpoint GET
def select_query_db(query, args=()):
    cursor = get_db_connection().execute(query, args)
    result_set = cursor.fetchall()
    cursor.close()
    return result_set

# Padronizando requests para endpoint POST e UPDATE
def insert_update_query_db(query, args=()):
    connection = get_db_connection()
    cursor = connection.cursor()
    result_set = cursor.execute(query, args)
    connection.commit()
    cursor.close()
    return result_set

def delete_query_db(query, args=()):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(query, args)
    connection.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    return rows_affected

# Busca todos os usuários
def get_usuarios():
    # Usando da função padrão para requests GET
    result_set = select_query_db('SELECT * FROM tb_usuario')
    # Retornando os usuário em Json atravez do dict function
    return [dict(data) for data in result_set]

# Busca um usuário pelo id
def get_usuario_by_id(user_id):
    # Usando da função padrão para requests GET
    result_set = select_query_db(f'SELECT * FROM tb_usuario WHERE id={user_id}')
    # Retornando os usuário em Json atravez do dict function
    return [dict(data) for data in result_set]

# Insere um novo usuário ao banco
def set_usuario(data):
    # Criação do usuário.
    nome = data.get('nome')
    nascimento = data.get('nascimento')

    # Usando da função padrão para requests POST
    # Persistir os dados no banco.
    result_set = insert_update_query_db(
        'INSERT INTO tb_usuario(nome, nascimento) VALUES (?, ?)',
        (nome, nascimento)
    )

    data['id'] = result_set.lastrowid
    # Retornar o usuário criado.
    return {"message": "Successfully created user", "data": data}

# Atualiza os dados de um usuário pelo id
def update_usuario_by_id(data, user_id):
    # Criação do usuário.
    nome = data.get('nome')
    nascimento = data.get('nascimento')

    # Persistir os dados no banco.
    result_set = insert_update_query_db(
        'UPDATE tb_usuario SET nome=?, nascimento=? WHERE id=?',
        (nome, nascimento, user_id)
    )

    # Retornar o usuário atualizado.
    data['id'] = user_id
    return {"message": "Successfully updated user", "data": data}

def delete_usuario(user_id):
    # Persistir os dados no banco.
    rows_deleted = delete_query_db(
        'DELETE FROM tb_usuario WHERE id=?',
        (user_id,)
    )
    
    # Retornar o usuário atualizado.
    if rows_deleted > 0:
        return {"message": f"Usuário {user_id} excluído com sucesso"}

    # Retorna caso não encontre um usuário
    return {"message": "Usuário não encontrado"}

@app.route("/")
def index():
    return jsonify({"versao": 1}), 200

@app.route("/usuarios", methods=['GET', 'POST'])
def usuarios():
    if request.method == 'GET':
        # Listagem dos usuários
        usuarios = get_usuarios()
        if usuarios is not None:
            return jsonify(usuarios), 200
        return jsonify({"message": "Bad request"}), 404

    elif request.method == 'POST':
        # Recuperar dados da requisição: json.
        data = request.json
        data = set_usuario(data)
        if data is not None:
            return jsonify(data), 201
        return jsonify({"message": "Bad request"}), 404

@app.route("/usuarios/<int:user_id>", methods=['GET', 'DELETE', 'PUT'])
def usuario(user_id):
    if request.method == 'GET':
        # Listagem de usuário por ID
        usuario = get_usuario_by_id(user_id)
        if usuario is not None:
            return jsonify(usuario), 200
        return jsonify({"message": "Bad request"}), 404

    if request.method == 'PUT':
        # Update do usuário por ID
        data = request.get_json()
        usuario = update_usuario_by_id(data, user_id)
        if usuario is not None:
            return jsonify(usuario), 200
        return jsonify({"message": "Bad request"}), 404

    if request.method == 'DELETE':
        # Delete do usuário por ID
        usuario = delete_usuario(user_id)
        if usuario is not None:
            return jsonify(usuario), 200
        return jsonify({"message": "Bad request"}), 404
