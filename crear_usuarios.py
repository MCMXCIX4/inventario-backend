from app import app, db
from models import Usuario

with app.app_context():
    admin = Usuario(email='admin@empresa.com', contraseña='admin123', rol='admin')
    vendedor = Usuario(email='vendedor@empresa.com', contraseña='venta123', rol='vendedor')

    db.session.add(admin)
    db.session.add(vendedor)
    db.session.commit()

    print("Usuarios creados exitosamente.")
