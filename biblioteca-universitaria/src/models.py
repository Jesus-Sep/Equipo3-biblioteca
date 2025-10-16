from datetime import datetime
from src.extensions import db

class Libro(db.Model):
    __tablename__ = "libros"
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(120), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    editorial = db.Column(db.String(100))
    año_publicacion = db.Column(db.Integer)
    categoria = db.Column(db.String(50))
    ejemplares_totales = db.Column(db.Integer, default=1)
    ejemplares_disponibles = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    prestamos = db.relationship('Prestamo', backref='libro', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'autor': self.autor,
            'isbn': self.isbn,
            'editorial': self.editorial,
            'año_publicacion': self.año_publicacion,
            'categoria': self.categoria,
            'ejemplares_totales': self.ejemplares_totales,
            'ejemplares_disponibles': self.ejemplares_disponibles,
            'created_at': self.created_at.isoformat()
        }

class Estudiante(db.Model):
    __tablename__ = "estudiantes"
    
    id = db.Column(db.Integer, primary_key=True)
    codigo_estudiante = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    apellido = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    carrera = db.Column(db.String(100))
    semestre = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    prestamos = db.relationship('Prestamo', backref='estudiante', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo_estudiante': self.codigo_estudiante,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'carrera': self.carrera,
            'semestre': self.semestre,
            'created_at': self.created_at.isoformat()
        }

class Prestamo(db.Model):
    __tablename__ = "prestamos"
    
    id = db.Column(db.Integer, primary_key=True)
    libro_id = db.Column(db.Integer, db.ForeignKey('libros.id'), nullable=False)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    fecha_prestamo = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fecha_devolucion_esperada = db.Column(db.DateTime, nullable=False)
    fecha_devolucion_real = db.Column(db.DateTime)
    estado = db.Column(db.String(20), default='activo')  # activo, devuelto, vencido
    
    def to_dict(self):
        return {
            'id': self.id,
            'libro_id': self.libro_id,
            'estudiante_id': self.estudiante_id,
            'fecha_prestamo': self.fecha_prestamo.isoformat(),
            'fecha_devolucion_esperada': self.fecha_devolucion_esperada.isoformat(),
            'fecha_devolucion_real': self.fecha_devolucion_real.isoformat() if self.fecha_devolucion_real else None,
            'estado': self.estado
        }