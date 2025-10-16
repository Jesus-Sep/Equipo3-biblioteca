import uuid
from datetime import datetime
from src.extensions import db

class Usuario(db.Model):
    __tablename__ = "usuarios"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20), default="")
    activo = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def actualizar_info(self, nombre: str = None, telefono: str = None):
        if nombre:
            self.nombre = nombre
        if telefono:
            self.telefono = telefono
    
    def desactivar(self):
        self.activo = False
    
    def __str__(self):
        return f"Usuario: {self.nombre} ({self.email}) - {'Activo' if self.activo else 'Inactivo'}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'activo': self.activo,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }