from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Producto, Usuario, Prediccion

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "API Inventario Activa"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = Usuario.query.filter_by(email=data['email'], contraseña=data['contraseña']).first()
    if usuario:
        return jsonify({
            'id': usuario.id,
            'email': usuario.email,
            'rol': usuario.rol
        })
    else:
        return jsonify({'error': 'Credenciales inválidas'}), 401

@app.route('/productos', methods=['GET'])
def get_productos():
    productos = Producto.query.all()
    return jsonify([{
        'id': p.id,
        'nombre': p.nombre,
        'cantidad': p.cantidad,
        'categoria': p.categoria
    } for p in productos])

@app.route('/productos', methods=['POST'])
def add_producto():
    data = request.json
    nuevo = Producto(
        nombre=data['nombre'],
        cantidad=data['cantidad'],
        categoria=data.get('categoria')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Producto agregado'}), 201

@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def delete_producto(producto_id):
    producto = Producto.query.get(producto_id)
    if producto:
        db.session.delete(producto)
        db.session.commit()
        return jsonify({'mensaje': 'Producto eliminado'})
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404


@app.route('/alertas', methods=['GET'])
def alertas_stock_bajo():
    productos_bajo_stock = Producto.query.filter(Producto.cantidad < 5).all()
    return jsonify([
        {
            'id': p.id,
            'nombre': p.nombre,
            'cantidad': p.cantidad,
            'categoria': p.categoria
        } for p in productos_bajo_stock
    ])

@app.route('/predicciones', methods=['POST'])
def agregar_prediccion():
    data = request.json
    pred = Prediccion(
        producto_id=data['producto_id'],
        cantidad_estimado=data['cantidad_estimado'],
        fecha=data['fecha']
    )
    db.session.add(pred)
    db.session.commit()
    return jsonify({'mensaje': 'Predicción registrada'}), 201

@app.route('/predicciones', methods=['GET'])
def ver_predicciones():
    predicciones = Prediccion.query.all()
    return jsonify([
        {
            'id': p.id,
            'producto_id': p.producto_id,
            'cantidad_estimado': p.cantidad_estimado,
            'fecha': p.fecha
        } for p in predicciones
    ])

@app.route('/predicciones/<int:prediccion_id>', methods=['DELETE'])
def eliminar_prediccion(prediccion_id):
    pred = Prediccion.query.get(prediccion_id)
    if pred:
        db.session.delete(pred)
        db.session.commit()
        return jsonify({'mensaje': 'Predicción eliminada'})
    else:
        return jsonify({'error': 'Predicción no encontrada'}), 404

if __name__ == '__main__':
    app.run(debug=True)
