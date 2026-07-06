from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import os
import json

# ==================== CONFIGURAÇÃO ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), 'frontend')
STATIC_DIR = os.path.join(FRONTEND_DIR, 'static')

app = Flask(__name__, 
            static_folder=STATIC_DIR,
            template_folder=FRONTEND_DIR)

# Habilita CORS
CORS(app)

# ==================== SWAGGER CONFIGURATION ====================
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "PetLembra API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# ==================== GERAR SWAGGER.JSON ====================
def generate_swagger_json():
    """Gera o arquivo swagger.json com a documentação completa da API"""
    
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)
    
    swagger_doc = {
        "openapi": "3.0.0",
        "info": {
            "title": "PetLembra API",
            "description": "🐾 API RESTful para gerenciamento de pets e agendamentos.",
            "version": "1.0.0",
            "contact": {
                "name": "Suporte PetLembra",
                "email": "suporte@petlembra.com"
            }
        },
        "servers": [
            {
                "url": "http://localhost:5000",
                "description": "Servidor de Desenvolvimento"
            }
        ],
        "tags": [
            {"name": "Clientes", "description": "Operações relacionadas a clientes"},
            {"name": "Pets", "description": "Operações relacionadas a pets"},
            {"name": "Agendamentos", "description": "Operações relacionadas a agendamentos"},
            {"name": "Dashboard", "description": "Dados para o dashboard"}
        ],
        "paths": {
            "/api/dashboard": {
                "get": {
                    "tags": ["Dashboard"],
                    "summary": "Dados para o dashboard",
                    "responses": {
                        "200": {
                            "description": "Dados do dashboard retornados com sucesso"
                        }
                    }
                }
            },
            "/api/clientes": {
                "get": {
                    "tags": ["Clientes"],
                    "summary": "Lista todos os clientes",
                    "responses": {
                        "200": {
                            "description": "Lista de clientes retornada com sucesso"
                        }
                    }
                },
                "post": {
                    "tags": ["Clientes"],
                    "summary": "Cria um novo cliente",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["nome", "telefone"],
                                    "properties": {
                                        "nome": {"type": "string"},
                                        "telefone": {"type": "string"},
                                        "email": {"type": "string"},
                                        "endereco": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {"description": "Cliente criado com sucesso"},
                        "400": {"description": "Dados inválidos"}
                    }
                }
            },
            "/api/clientes/{id}": {
                "get": {
                    "tags": ["Clientes"],
                    "summary": "Busca um cliente por ID",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "ID do cliente"
                        }
                    ],
                    "responses": {
                        "200": {"description": "Cliente encontrado"},
                        "404": {"description": "Cliente não encontrado"}
                    }
                },
                "put": {
                    "tags": ["Clientes"],
                    "summary": "Atualiza um cliente",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "ID do cliente"
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["nome", "telefone"],
                                    "properties": {
                                        "nome": {"type": "string"},
                                        "telefone": {"type": "string"},
                                        "email": {"type": "string"},
                                        "endereco": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Cliente atualizado com sucesso"},
                        "404": {"description": "Cliente não encontrado"}
                    }
                },
                "delete": {
                    "tags": ["Clientes"],
                    "summary": "Remove um cliente",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "ID do cliente"
                        }
                    ],
                    "responses": {
                        "200": {"description": "Cliente removido com sucesso"},
                        "404": {"description": "Cliente não encontrado"}
                    }
                }
            },
            "/api/pets": {
                "get": {
                    "tags": ["Pets"],
                    "summary": "Lista todos os pets",
                    "responses": {
                        "200": {
                            "description": "Lista de pets retornada com sucesso"
                        }
                    }
                },
                "post": {
                    "tags": ["Pets"],
                    "summary": "Cria um novo pet",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["nome", "especie", "cliente_id"],
                                    "properties": {
                                        "nome": {"type": "string"},
                                        "especie": {"type": "string"},
                                        "raca": {"type": "string"},
                                        "idade": {"type": "integer"},
                                        "observacoes": {"type": "string"},
                                        "cliente_id": {"type": "integer"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {"description": "Pet criado com sucesso"},
                        "400": {"description": "Dados inválidos"}
                    }
                }
            },
            "/api/pets/{id}": {
                "get": {
                    "tags": ["Pets"],
                    "summary": "Busca um pet por ID",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "ID do pet"
                        }
                    ],
                    "responses": {
                        "200": {"description": "Pet encontrado"},
                        "404": {"description": "Pet não encontrado"}
                    }
                },
                "put": {
                    "tags": ["Pets"],
                    "summary": "Atualiza um pet",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "ID do pet"
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["nome", "especie", "cliente_id"],
                                    "properties": {
                                        "nome": {"type": "string"},
                                        "especie": {"type": "string"},
                                        "raca": {"type": "string"},
                                        "idade": {"type": "integer"},
                                        "observacoes": {"type": "string"},
                                        "cliente_id": {"type": "integer"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Pet atualizado com sucesso"},
                        "404": {"description": "Pet não encontrado"}
                    }
                },
                "delete": {
                    "tags": ["Pets"],
                    "summary": "Remove um pet",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "ID do pet"
                        }
                    ],
                    "responses": {
                        "200": {"description": "Pet removido com sucesso"},
                        "404": {"description": "Pet não encontrado"}
                    }
                }
            },
            "/api/pets/cliente/{cliente_id}": {
                "get": {
                    "tags": ["Pets"],
                    "summary": "Lista pets por cliente",
                    "parameters": [
                        {
                            "name": "cliente_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "ID do cliente"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Lista de pets do cliente"
                        }
                    }
                }
            },
            "/api/agendamentos": {
                "get": {
                    "tags": ["Agendamentos"],
                    "summary": "Lista agendamentos com filtros",
                    "parameters": [
                        {
                            "name": "status",
                            "in": "query",
                            "required": False,
                            "schema": {
                                "type": "string",
                                "enum": ["agendado", "concluido", "cancelado"]
                            },
                            "description": "Filtrar por status do agendamento"
                        },
                        {
                            "name": "data",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string", "format": "date"},
                            "description": "Filtrar por data (formato YYYY-MM-DD)"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Lista de agendamentos retornada com sucesso"
                        }
                    }
                },
                "post": {
                    "tags": ["Agendamentos"],
                    "summary": "Cria um novo agendamento",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["pet_id", "data", "tipo"],
                                    "properties": {
                                        "pet_id": {"type": "integer"},
                                        "data": {"type": "string", "format": "date"},
                                        "tipo": {"type": "string"},
                                        "valor": {"type": "number", "format": "float"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {"description": "Agendamento criado com sucesso"},
                        "400": {"description": "Dados inválidos"}
                    }
                }
            },
            "/api/agendamentos/{id}": {
                "get": {
                    "tags": ["Agendamentos"],
                    "summary": "Busca um agendamento por ID",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "ID do agendamento"
                        }
                    ],
                    "responses": {
                        "200": {"description": "Agendamento encontrado"},
                        "404": {"description": "Agendamento não encontrado"}
                    }
                },
                "put": {
                    "tags": ["Agendamentos"],
                    "summary": "Atualiza um agendamento",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "ID do agendamento"
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["pet_id", "data", "tipo", "status"],
                                    "properties": {
                                        "pet_id": {"type": "integer"},
                                        "data": {"type": "string", "format": "date"},
                                        "tipo": {"type": "string"},
                                        "valor": {"type": "number"},
                                        "status": {"type": "string", "enum": ["agendado", "concluido", "cancelado"]}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Agendamento atualizado com sucesso"},
                        "404": {"description": "Agendamento não encontrado"}
                    }
                },
                "delete": {
                    "tags": ["Agendamentos"],
                    "summary": "Remove um agendamento",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "ID do agendamento"
                        }
                    ],
                    "responses": {
                        "200": {"description": "Agendamento removido com sucesso"},
                        "404": {"description": "Agendamento não encontrado"}
                    }
                }
            },
            "/api/agendamentos/{id}/status": {
                "patch": {
                    "tags": ["Agendamentos"],
                    "summary": "Atualiza status do agendamento",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "ID do agendamento"
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["status"],
                                    "properties": {
                                        "status": {
                                            "type": "string",
                                            "enum": ["agendado", "concluido", "cancelado"],
                                            "description": "Novo status do agendamento"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Status atualizado com sucesso"},
                        "404": {"description": "Agendamento não encontrado"}
                    }
                }
            },
            "/api/agendamentos/hoje": {
                "get": {
                    "tags": ["Agendamentos"],
                    "summary": "Lista agendamentos de hoje",
                    "responses": {
                        "200": {
                            "description": "Lista de agendamentos de hoje"
                        }
                    }
                }
            },
            "/api/agendamentos/pet/{pet_id}": {
                "get": {
                    "tags": ["Agendamentos"],
                    "summary": "Lista agendamentos por pet",
                    "parameters": [
                        {
                            "name": "pet_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                            "description": "ID do pet"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Lista de agendamentos do pet"
                        }
                    }
                }
            }
        }
    }
    
    swagger_path = os.path.join(STATIC_DIR, 'swagger.json')
    with open(swagger_path, 'w', encoding='utf-8') as f:
        json.dump(swagger_doc, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Swagger.json gerado em: {swagger_path}")

# ==================== IMPORTAR MODELOS ====================
from database import init_db
import models

# ==================== INICIALIZAÇÃO ====================
init_db()
generate_swagger_json()

# ==================== ROTAS PARA O FRONTEND ====================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename)

# ==================== DASHBOARD API ====================
@app.route('/api/dashboard', methods=['GET'])
def api_dashboard():
    try:
        agendamentos_hoje = models.get_agendamentos_hoje()
        clientes = models.listar_clientes()
        pets = models.listar_todos_pets()
        
        return jsonify({
            'total_clientes': len(clientes),
            'total_pets': len(pets),
            'agendamentos_hoje': [dict(ag) for ag in agendamentos_hoje],
            'clientes': [dict(c) for c in clientes],
            'pets': [dict(p) for p in pets]
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# ==================== API REST - CLIENTES ====================
@app.route('/api/clientes', methods=['GET'])
def api_listar_clientes():
    try:
        clientes = models.listar_clientes()
        return jsonify([dict(cliente) for cliente in clientes])
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/clientes/<int:id>', methods=['GET'])
def api_buscar_cliente(id):
    try:
        cliente = models.buscar_cliente_por_id(id)
        if cliente:
            return jsonify(dict(cliente))
        return jsonify({'erro': 'Cliente não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/clientes', methods=['POST'])
def api_criar_cliente():
    try:
        data = request.json
        if not data.get('nome'):
            return jsonify({'erro': 'Nome é obrigatório'}), 400
        if not data.get('telefone'):
            return jsonify({'erro': 'Telefone é obrigatório'}), 400
        
        cliente_id = models.criar_cliente(
            data['nome'],
            data['telefone'],
            data.get('email', ''),
            data.get('endereco', '')
        )
        return jsonify({'id': cliente_id, 'mensagem': 'Cliente criado com sucesso'}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/api/clientes/<int:id>', methods=['PUT'])
def api_atualizar_cliente(id):
    try:
        data = request.json
        cliente = models.buscar_cliente_por_id(id)
        if not cliente:
            return jsonify({'erro': 'Cliente não encontrado'}), 404
        
        models.atualizar_cliente(
            id,
            data['nome'],
            data['telefone'],
            data.get('email', ''),
            data.get('endereco', '')
        )
        return jsonify({'mensagem': 'Cliente atualizado com sucesso'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/api/clientes/<int:id>', methods=['DELETE'])
def api_deletar_cliente(id):
    try:
        cliente = models.buscar_cliente_por_id(id)
        if not cliente:
            return jsonify({'erro': 'Cliente não encontrado'}), 404
        
        models.deletar_cliente(id)
        return jsonify({'mensagem': 'Cliente removido com sucesso'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

# ==================== API REST - PETS ====================
@app.route('/api/pets', methods=['GET'])
def api_listar_pets():
    try:
        pets = models.listar_todos_pets()
        return jsonify([dict(pet) for pet in pets])
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/pets/cliente/<int:cliente_id>', methods=['GET'])
def api_listar_pets_por_cliente(cliente_id):
    try:
        pets = models.listar_pets_por_cliente(cliente_id)
        return jsonify([dict(pet) for pet in pets])
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/pets/<int:id>', methods=['GET'])
def api_buscar_pet(id):
    try:
        pet = models.buscar_pet_por_id(id)
        if pet:
            return jsonify(dict(pet))
        return jsonify({'erro': 'Pet não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/pets', methods=['POST'])
def api_criar_pet():
    try:
        data = request.json
        if not data.get('nome'):
            return jsonify({'erro': 'Nome é obrigatório'}), 400
        if not data.get('especie'):
            return jsonify({'erro': 'Espécie é obrigatória'}), 400
        if not data.get('cliente_id'):
            return jsonify({'erro': 'Cliente é obrigatório'}), 400
        
        pet_id = models.criar_pet(
            data['nome'],
            data['especie'],
            data.get('raca', ''),
            data.get('idade'),
            data.get('observacoes', ''),
            data['cliente_id']
        )
        return jsonify({'id': pet_id, 'mensagem': 'Pet criado com sucesso'}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/api/pets/<int:id>', methods=['PUT'])
def api_atualizar_pet(id):
    try:
        data = request.json
        pet = models.buscar_pet_por_id(id)
        if not pet:
            return jsonify({'erro': 'Pet não encontrado'}), 404
        
        models.atualizar_pet(
            id,
            data['nome'],
            data['especie'],
            data.get('raca', ''),
            data.get('idade'),
            data.get('observacoes', ''),
            data['cliente_id']
        )
        return jsonify({'mensagem': 'Pet atualizado com sucesso'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/api/pets/<int:id>', methods=['DELETE'])
def api_deletar_pet(id):
    try:
        pet = models.buscar_pet_por_id(id)
        if not pet:
            return jsonify({'erro': 'Pet não encontrado'}), 404
        
        models.deletar_pet(id)
        return jsonify({'mensagem': 'Pet removido com sucesso'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

# ==================== API REST - AGENDAMENTOS ====================
@app.route('/api/agendamentos', methods=['GET'])
def api_listar_agendamentos():
    try:
        status = request.args.get('status')
        data = request.args.get('data')
        agendamentos = models.listar_agendamentos(status, data)
        return jsonify([dict(ag) for ag in agendamentos])
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/agendamentos/hoje', methods=['GET'])
def api_agendamentos_hoje():
    try:
        agendamentos = models.get_agendamentos_hoje()
        return jsonify([dict(ag) for ag in agendamentos])
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/agendamentos/pet/<int:pet_id>', methods=['GET'])
def api_agendamentos_por_pet(pet_id):
    try:
        agendamentos = models.listar_agendamentos_por_pet(pet_id)
        return jsonify([dict(ag) for ag in agendamentos])
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/agendamentos/<int:id>', methods=['GET'])
def api_buscar_agendamento(id):
    try:
        agendamento = models.buscar_agendamento_por_id(id)
        if agendamento:
            return jsonify(dict(agendamento))
        return jsonify({'erro': 'Agendamento não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/agendamentos', methods=['POST'])
def api_criar_agendamento():
    try:
        data = request.json
        if not data.get('pet_id'):
            return jsonify({'erro': 'Pet é obrigatório'}), 400
        if not data.get('data'):
            return jsonify({'erro': 'Data é obrigatória'}), 400
        if not data.get('tipo'):
            return jsonify({'erro': 'Tipo de serviço é obrigatório'}), 400
        
        agendamento_id = models.criar_agendamento(
            data['data'],
            data['tipo'],
            data.get('valor'),
            data['pet_id']
        )
        return jsonify({'id': agendamento_id, 'mensagem': 'Agendamento criado com sucesso'}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/api/agendamentos/<int:id>', methods=['PUT'])
def api_atualizar_agendamento(id):
    try:
        data = request.json
        agendamento = models.buscar_agendamento_por_id(id)
        if not agendamento:
            return jsonify({'erro': 'Agendamento não encontrado'}), 404
        
        models.atualizar_agendamento(
            id,
            data['data'],
            data['tipo'],
            data.get('valor'),
            data['status'],
            data['pet_id']
        )
        return jsonify({'mensagem': 'Agendamento atualizado com sucesso'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/api/agendamentos/<int:id>/status', methods=['PATCH'])
def api_atualizar_status_agendamento(id):
    try:
        data = request.json
        agendamento = models.buscar_agendamento_por_id(id)
        if not agendamento:
            return jsonify({'erro': 'Agendamento não encontrado'}), 404
        if not data.get('status'):
            return jsonify({'erro': 'Status é obrigatório'}), 400
        
        models.atualizar_status_agendamento(id, data['status'])
        return jsonify({'mensagem': 'Status atualizado com sucesso'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/api/agendamentos/<int:id>', methods=['DELETE'])
def api_deletar_agendamento(id):
    try:
        agendamento = models.buscar_agendamento_por_id(id)
        if not agendamento:
            return jsonify({'erro': 'Agendamento não encontrado'}), 404
        
        models.deletar_agendamento(id)
        return jsonify({'mensagem': 'Agendamento removido com sucesso'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)