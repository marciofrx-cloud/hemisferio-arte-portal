# backend/models.py

from flask_sqlalchemy import SQLAlchemy

# Inicializa a instância do SQLAlchemy sem associar a um app ainda
# Isso será feito no app.py usando db.init_app(app)
db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    file_path = db.Column(db.String(200), nullable=True) # Caminho para o arquivo digital
    image_path = db.Column(db.String(200), nullable=True) # Caminho para a imagem de capa

    def __repr__(self):
        return f'<Product {self.name}>'

