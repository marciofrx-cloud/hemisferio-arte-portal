# backend/add_products.py

import os
from flask import Flask
from models import db, Product # Importa db e Product de models.py

# ========================================
# CONFIGURAÇÃO DO FLASK (PARA USO TEMPORÁRIO NESTE SCRIPT)
# ========================================
app = Flask(__name__)

# Define o caminho absoluto para a pasta 'instance'
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
db_path = os.path.join(instance_path, 'site.db')

# Garante que a pasta 'instance' exista
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Associa o banco de dados ao app para este script
db.init_app(app)

# ========================================
# CRIAÇÃO DO BANCO DE DADOS E ADIÇÃO DE PRODUTOS
# ========================================
with app.app_context():
    # Remove o banco de dados existente para garantir uma recriação limpa
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Banco de dados existente removido: {db_path}")

    db.create_all() # Cria as tabelas no banco de dados

    # Adiciona produtos de teste
    product1 = Product(name='Música Épica - A Jornada', price=19.90, file_path='downloads/musica_epica.mp3', image_path='images/musica_epica.jpg')
    product2 = Product(name='Audiobook - O Segredo do Farol', price=34.50, file_path='downloads/audiobook_farol.mp3', image_path='images/audiobook_farol.jpg')
    product3 = Product(name='Trilha Sonora - Floresta Encantada', price=25.00, file_path='downloads/trilha_sonora.mp3', image_path='images/trilha_sonora.jpg')

    db.session.add_all([product1, product2, product3])
    db.session.commit()

    print("Produtos de teste adicionados ao banco de dados!")

