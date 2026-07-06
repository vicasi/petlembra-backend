from database import get_db_connection
from datetime import datetime

# ==================== CLIENTES ====================
def listar_clientes():
    conn = get_db_connection()
    clientes = conn.execute('SELECT * FROM clientes ORDER BY nome').fetchall()
    conn.close()
    return clientes

def buscar_cliente_por_id(id):
    conn = get_db_connection()
    cliente = conn.execute('SELECT * FROM clientes WHERE id = ?', (id,)).fetchone()
    conn.close()
    return cliente

def criar_cliente(nome, telefone, email, endereco):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clientes (nome, telefone, email, endereco)
        VALUES (?, ?, ?, ?)
    ''', (nome, telefone, email, endereco))
    conn.commit()
    cliente_id = cursor.lastrowid
    conn.close()
    return cliente_id

def atualizar_cliente(id, nome, telefone, email, endereco):
    conn = get_db_connection()
    conn.execute('''
        UPDATE clientes 
        SET nome = ?, telefone = ?, email = ?, endereco = ?
        WHERE id = ?
    ''', (nome, telefone, email, endereco, id))
    conn.commit()
    conn.close()

def deletar_cliente(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM clientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# ==================== PETS ====================
def listar_pets_por_cliente(cliente_id):
    conn = get_db_connection()
    pets = conn.execute('''
        SELECT p.*, c.nome as dono_nome 
        FROM pets p
        JOIN clientes c ON p.cliente_id = c.id
        WHERE p.cliente_id = ?
        ORDER BY p.nome
    ''', (cliente_id,)).fetchall()
    conn.close()
    return pets

def listar_todos_pets():
    conn = get_db_connection()
    pets = conn.execute('''
        SELECT p.*, c.nome as dono_nome 
        FROM pets p
        JOIN clientes c ON p.cliente_id = c.id
        ORDER BY p.nome
    ''').fetchall()
    conn.close()
    return pets

def buscar_pet_por_id(id):
    conn = get_db_connection()
    pet = conn.execute('SELECT * FROM pets WHERE id = ?', (id,)).fetchone()
    conn.close()
    return pet

def criar_pet(nome, especie, raca, idade, observacoes, cliente_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pets (nome, especie, raca, idade, observacoes, cliente_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, especie, raca, idade, observacoes, cliente_id))
    conn.commit()
    pet_id = cursor.lastrowid
    conn.close()
    return pet_id

def atualizar_pet(id, nome, especie, raca, idade, observacoes, cliente_id):
    conn = get_db_connection()
    conn.execute('''
        UPDATE pets 
        SET nome = ?, especie = ?, raca = ?, idade = ?, observacoes = ?, cliente_id = ?
        WHERE id = ?
    ''', (nome, especie, raca, idade, observacoes, cliente_id, id))
    conn.commit()
    conn.close()

def deletar_pet(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM pets WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# ==================== AGENDAMENTOS ====================
def listar_agendamentos(filtro_status=None, filtro_data=None):
    conn = get_db_connection()
    
    query = '''
        SELECT a.*, p.nome as pet_nome, c.nome as cliente_nome, c.telefone
        FROM agendamentos a
        JOIN pets p ON a.pet_id = p.id
        JOIN clientes c ON p.cliente_id = c.id
        WHERE 1=1
    '''
    params = []
    
    if filtro_status:
        query += ' AND a.status = ?'
        params.append(filtro_status)
    
    if filtro_data:
        query += ' AND a.data = ?'
        params.append(filtro_data)
    
    query += ' ORDER BY a.data ASC'
    
    agendamentos = conn.execute(query, params).fetchall()
    conn.close()
    return agendamentos

def listar_agendamentos_por_pet(pet_id):
    conn = get_db_connection()
    agendamentos = conn.execute('''
        SELECT a.*, p.nome as pet_nome 
        FROM agendamentos a
        JOIN pets p ON a.pet_id = p.id
        WHERE a.pet_id = ?
        ORDER BY a.data DESC
    ''', (pet_id,)).fetchall()
    conn.close()
    return agendamentos

def buscar_agendamento_por_id(id):
    conn = get_db_connection()
    agendamento = conn.execute('SELECT * FROM agendamentos WHERE id = ?', (id,)).fetchone()
    conn.close()
    return agendamento

def criar_agendamento(data, tipo, valor, pet_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO agendamentos (data, tipo, valor, status, pet_id)
        VALUES (?, ?, ?, 'agendado', ?)
    ''', (data, tipo, valor, pet_id))
    conn.commit()
    agendamento_id = cursor.lastrowid
    conn.close()
    return agendamento_id

def atualizar_agendamento(id, data, tipo, valor, status, pet_id):
    conn = get_db_connection()
    conn.execute('''
        UPDATE agendamentos 
        SET data = ?, tipo = ?, valor = ?, status = ?, pet_id = ?
        WHERE id = ?
    ''', (data, tipo, valor, status, pet_id, id))
    conn.commit()
    conn.close()

def deletar_agendamento(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM agendamentos WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def atualizar_status_agendamento(id, novo_status):
    conn = get_db_connection()
    conn.execute('UPDATE agendamentos SET status = ? WHERE id = ?', (novo_status, id))
    conn.commit()
    conn.close()

def get_agendamentos_hoje():
    hoje = datetime.now().strftime('%Y-%m-%d')
    return listar_agendamentos(filtro_data=hoje)