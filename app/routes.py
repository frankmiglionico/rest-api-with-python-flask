from app import app
from etc import data

from flask import render_template, jsonify, request

@app.route('/')
@app.route('/index')
def index():
    user = 'Frank'
    return render_template('index.html', title='This', user=user)

@app.route('/produtos/all')
def produtos_all():
    jsonify(data.produtos)

@app.route('/produtos')
def produtos_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return jsonify({'error': 'Missing parameters'})

    results = []

    for produto in data.produtos:
        if produto['id'] == id:
            results.append(produto)

    if not results:
        return jsonify({'error': 'ID not found'})

    return jsonify(results)

@app.route('/vendas/all')
def vendas_all():
    jsonify(data.vendas)

@app.route('/vendas')
def vendas_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return jsonify({'error': 'Missing parameters'})

    results = []

    for venda in data.vendas:
        if venda['id'] == id:
            results.append(venda)

    if not results:
        return jsonify({'error': 'ID not found'})

    return jsonify(results)

@app.route('/clientes/all')
def clientes_all():
    jsonify(data.clientes)

@app.route('/clientes')
def clientes_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return jsonify({'error': 'Missing parameters'})

    results = []

    for cliente in data.clientes:
        if cliente['id'] == id:
            results.append(cliente)

    if not results:
        return jsonify({'error': 'ID not found'})

    return jsonify(results)