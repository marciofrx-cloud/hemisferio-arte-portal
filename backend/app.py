# backend/app.py

import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Product

# ========================================
# CONFIGURAÇÃO DO FLASK
# ========================================
app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.config['SECRET_KEY'] = 'sua_chave_secreta_super_segura_aqui'

# Define o caminho absoluto para a pasta 'instance' e o arquivo do banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
db_path = os.path.join(instance_path, 'site.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados com o app
db.init_app(app)

# ========================================
# ROTAS
# ========================================

@app.route('/')
def index():
    """Página inicial - exibe todos os produtos"""
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    """Adiciona um produto ao carrinho"""
    product = Product.query.get_or_404(product_id)

    # Inicializa o carrinho na sessão se não existir
    if 'cart' not in session:
        session['cart'] = []

    cart = session['cart']

    # Verifica se o produto já está no carrinho
    product_in_cart = False
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1
            product_in_cart = True
            break

    # Se o produto não está no carrinho, adiciona
    if not product_in_cart:
        cart.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'image_path': product.image_path,
            'quantity': 1
        })

    session['cart'] = cart
    flash('Produto adicionado ao carrinho!', 'success')
    return redirect(url_for('index'))

@app.route('/cart')
def view_cart():
    """Exibe o carrinho de compras"""
    cart = session.get('cart', [])

    # Calcula o total de cada item e o total geral
    total_price = 0
    for item in cart:
        item['item_total'] = item['price'] * item['quantity']
        total_price += item['item_total']

    return render_template('cart.html', cart_items=cart, total_price=total_price)

@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    """Atualiza a quantidade de um produto no carrinho"""
    quantity = int(request.form.get('quantity', 1))

    if quantity < 1:
        flash('Quantidade inválida.', 'danger')
        return redirect(url_for('view_cart'))

    cart = session.get('cart', [])

    for item in cart:
        if item['id'] == product_id:
            item['quantity'] = quantity
            break

    session['cart'] = cart
    flash('Quantidade atualizada!', 'success')
    return redirect(url_for('view_cart'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    """Remove um produto do carrinho"""
    cart = session.get('cart', [])

    # Remove o produto do carrinho
    try:
        for item in cart:
            if item['id'] == product_id:
                cart.remove(item)
                flash('Item removido do carrinho!', 'info')
                break
        else:
            del cart[str(product_id)]
            flash('Item removido do carrinho!', 'info')
    except (ValueError, KeyError):
        flash('Quantidade inválida.', 'danger')

    session['cart'] = cart
    return redirect(url_for('view_cart'))

# ========================================
# EXECUÇÃO DO SERVIDOR
# ========================================
if __name__ == '__main__':
    app.run(debug=True)
