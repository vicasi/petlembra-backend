import sqlite3
import os
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'petlembra.db')

def populate_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    print("🌱 Populando banco de dados...")
    
    clientes = [
        ('Ana Paula Santos', '(11) 98765-4321', 'ana.santos@email.com', 'Rua das Flores, 123 - São Paulo, SP'),
        ('Carlos Eduardo Lima', '(11) 91234-5678', 'carlos.lima@email.com', 'Av. Paulista, 1000 - São Paulo, SP'),
        ('Mariana Oliveira Costa', '(21) 99876-5432', 'mariana.costa@email.com', 'Rua do Sol, 45 - Rio de Janeiro, RJ'),
        ('Roberto Almeida Souza', '(31) 98765-1234', 'roberto.almeida@email.com', 'Av. Amazonas, 500 - Belo Horizonte, MG'),
        ('Fernanda Rocha Mendes', '(41) 99988-7766', 'fernanda.mendes@email.com', 'Rua das Araucárias, 200 - Curitiba, PR'),
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO clientes (nome, telefone, email, endereco)
        VALUES (?, ?, ?, ?)
    ''', clientes)
    
    pets_data = [
        ('Thor', 'cachorro', 'Labrador', 3, 'Muito brincalhão, adora água', 1),
        ('Luna', 'gato', 'Siamês', 2, 'Arranha móveis, precisa de arranhador', 1),
        ('Bob', 'cachorro', 'Poodle', 5, 'Tem alergia a frango', 2),
        ('Mia', 'gato', 'Persa', 4, 'Toma banho semanal', 2),
        ('Rex', 'cachorro', 'Pastor Alemão', 6, 'Porte grande, muito dócil', 3),
        ('Mel', 'cachorro', 'SRD', 1, 'Filhote, muito energética', 3),
        ('Nina', 'gato', 'Frajola', 3, 'Medo de barulho', 4),
        ('Toby', 'cachorro', 'Shih Tzu', 2, 'Toma banho a cada 15 dias', 4),
        ('Bella', 'cachorro', 'Golden', 4, 'Adora brincar de buscar', 5),
        ('Luke', 'gato', 'Laranja', 5, 'Muito carinhoso', 5),
    ]
    
    for pet in pets_data:
        cursor.execute('''
            INSERT OR IGNORE INTO pets (nome, especie, raca, idade, observacoes, cliente_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', pet)
    
    hoje = datetime.now()
    hoje_str = hoje.strftime('%Y-%m-%d')
    amanha = (hoje + timedelta(days=1)).strftime('%Y-%m-%d')
    semana_passada = (hoje - timedelta(days=7)).strftime('%Y-%m-%d')
    
    agendamentos = [
        (hoje_str, 'banho', 60.00, 'agendado', 1),
        (hoje_str, 'consulta', 200.00, 'agendado', 3),
        (hoje_str, 'vacina', 120.00, 'agendado', 5),
        (hoje_str, 'tosa', 80.00, 'agendado', 7),
        (amanha, 'banho e tosa', 130.00, 'agendado', 2),
        (amanha, 'consulta', 250.00, 'agendado', 4),
        (amanha, 'vacina', 90.00, 'agendado', 6),
        (semana_passada, 'banho', 55.00, 'concluido', 2),
        (semana_passada, 'consulta', 180.00, 'concluido', 4),
        (semana_passada, 'tosa', 75.00, 'cancelado', 6),
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO agendamentos (data, tipo, valor, status, pet_id)
        VALUES (?, ?, ?, ?, ?)
    ''', agendamentos)
    
    conn.commit()
    
    cursor.execute('SELECT COUNT(*) FROM clientes')
    total_clientes = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM pets')
    total_pets = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM agendamentos')
    total_agendamentos = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"✅ {total_clientes} clientes cadastrados")
    print(f"✅ {total_pets} pets cadastrados")
    print(f"✅ {total_agendamentos} agendamentos cadastrados")
    print("🎉 Banco de dados populado com sucesso!")

if __name__ == '__main__':
    populate_database()