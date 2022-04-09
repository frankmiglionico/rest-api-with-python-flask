from app import app
from app.db import DB

from flask import render_template, jsonify, request

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/clientes', methods=['GET'])
def clientes():
    params = {}
    if 'id' in request.args:
        params['id'] = int(request.args['id'])
    elif 'nome' in request.args:
        params['nome'] = request.args['nome']
    else:
        return jsonify({'error': 'Missing parameters'})

    result = []
    
    db = DB()
    result = db.select_clientes(params=params)

    if not result:
        result = {'error': 'Cliente não encontrado'}

    return jsonify(result)

@app.route('/clientes/all', methods=['GET'])
def clientes_all():
    db = DB()
    return jsonify(db.select_clientes())

@app.route('/clientes/new', methods=['GET'])
def clientes_new():
    params = {}
    if 'nome' in request.args:
        params['nome'] = request.args['nome']
    else:
        return jsonify({'error': 'Missing parameters'})

    result = []

    db = DB()
    result = db.insert_cliente(params=params)

    if not result:
        result = {'error': 'Falha ao inserir'}

    return jsonify(result)

@app.route('/clientes/update', methods=['GET'])
def cliente_update():
    params = {}
    if 'id' in request.args and 'nome' in request.args:
        id = int(request.args['id'])
        params['nome'] = request.args['nome']
    else:
        return jsonify({'error': 'Missing parameters'})

    db = DB()
    return jsonify(db.execute_update(table='clientes', id=id, params=params))

@app.route('/clientes/delete', methods=['GET'])
def cliente_delete():
    params = {}
    if 'id' in request.args:
        params['id'] = int(request.args['id'])
    else:
        return jsonify({'error': 'Missing parameters'})

    db = DB()
    return jsonify(db.delete_cliente(params=params))

@app.route('/produtos', methods=['GET'])
def produtos():
    params = {}
    if 'id' in request.args:
        params['id'] = int(request.args['id'])
    elif 'descricao' in request.args:
        params['descricao'] = request.args['descricao']
    else:
        return jsonify({'error': 'Missing parameters'})

    result = []
    
    db = DB()
    result = db.select_produtos(params=params)

    if not result:
        result = {'error': 'Produto não encontrado'}

    return jsonify(result)

@app.route('/produtos/all', methods=['GET'])
def produtos_all():
    db = DB()
    return jsonify(db.select_produtos())

@app.route('/produtos/new', methods=['GET'])
def produtos_new():
    params = {}
    if 'descricao' in request.args:
        params['descricao'] = request.args['descricao']
    else:
        return jsonify({'error': 'Missing parameters'})

    result = []

    db = DB()
    result = db.insert_produto(params=params)

    if not result:
        result = {'error': 'Falha ao inserir'}

    return jsonify(result)

@app.route('/produtos/update', methods=['GET'])
def produtos_update():
    params = {}
    if 'id' in request.args and 'descricao' in request.args:
        id = int(request.args['id'])
        params['descricao'] = request.args['descricao']
    else:
        return jsonify({'error': 'Missing parameters'})

    db = DB()
    return jsonify(db.execute_update(table='produtos', id=id, params=params))

@app.route('/produtos/delete', methods=['GET'])
def produto_delete():
    params = {}
    if 'id' in request.args:
        params['id'] = int(request.args['id'])
    else:
        return jsonify({'error': 'Missing parameters'})

    db = DB()
    return jsonify(db.delete_produto(params=params))

@app.route('/vendas', methods=['GET'])
def vendas():
    params = {}
    if 'id' in request.args:
        params['id'] = int(request.args['id'])
    elif 'cliente_id' in request.args:
        params['cliente_id'] = request.args['cliente_id']
    elif 'produtos_id' in request.args:
        params['produtos_id'] = request.args['produtos_id']
    else:
        return jsonify({'error': 'Missing parameters'})

    result = []
    
    db = DB()
    result = db.select_vendas(params=params)

    if not result:
        result = {'error': 'Venda nao encontrada'}

    return jsonify(result)

@app.route('/vendas/all', methods=['GET'])
def vendas_all():    
    db = DB()
    return jsonify(db.select_vendas())

@app.route('/vendas/update', methods=['GET'])
def vendas_update():
    params = {}
    if 'id' in request.args and ('cliente_id' in request.args or 'produtos_id' in request.args):
        id = int(request.args['id'])
        if 'cliente_id' in request.args:
            params['cliente_id'] = request.args['cliente_id']
        if 'produtos_id' in request.args:
            params['produtos_id'] = request.args['produtos_id']
    else:
        return jsonify({'error': 'Missing parameters'})

    db = DB()
    return jsonify(db.execute_update(table='vendas', id=id, params=params))

@app.route('/vendas/delete', methods=['GET'])
def venda_delete():
    params = {}
    if 'id' in request.args:
        params['id'] = int(request.args['id'])
    else:
        return jsonify({'error': 'Missing parameters'})

    db = DB()
    return jsonify(db.delete_venda(params=params))