import uuid
from datetime import datetime, timedelta
from src.extensions import db

class Reserva(db.Model):
    __tablename__ = "reservas"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    usuario_id = db.Column(db.String(36), db.ForeignKey('usuarios.id'), nullable=False)
    libro_isbn = db.Column(db.String(20), db.ForeignKey('libros.isbn'), nullable=False)
    fecha_reserva = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_expiracion = db.Column(db.DateTime)
    estado = db.Column(db.String(20), default="activa")  # activa, expirada, cancelada, completada
    
    # Relaciones
    usuario = db.relationship('Usuario', backref='reservas')
    libro = db.relationship('Libro', backref='reservas')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.fecha_expiracion:
            self.fecha_expiracion = datetime.utcnow() + timedelta(days=3)
    
    def activar_reserva(self) -> bool:
        """Activa la reserva si el libro está disponible"""
        if self.libro and self.libro.disponible and self.estado == "activa":
            self.estado = 'completada'
            return True
        return False
    
    def cancelar_reserva(self):
        """Cancela la reserva"""
        self.estado = 'cancelada'
    
    def verificar_expiracion(self):
        """Verifica si la reserva ha expirado"""
        if self.estado == "activa" and datetime.utcnow() > self.fecha_expiracion:
            self.estado = 'expirada'
    
    def esta_activa(self) -> bool:
        """Verifica si la reserva está activa"""
        self.verificar_expiracion()
        return self.estado == "activa"
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'libro_isbn': self.libro_isbn,
            'fecha_reserva': self.fecha_reserva.isoformat() if self.fecha_reserva else None,
            'fecha_expiracion': self.fecha_expiracion.isoformat() if self.fecha_expiracion else None,
            'estado': self.estado
        }