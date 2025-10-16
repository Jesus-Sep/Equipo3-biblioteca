import uuid
from datetime import datetime, timedelta
from src.extensions import db

class Prestamo(db.Model):
    __tablename__ = "prestamos"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    usuario_id = db.Column(db.String(36), db.ForeignKey('usuarios.id'), nullable=False)
    libro_isbn = db.Column(db.String(20), db.ForeignKey('libros.isbn'), nullable=False)
    fecha_prestamo = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_devolucion_prevista = db.Column(db.DateTime)
    fecha_devolucion_real = db.Column(db.DateTime)
    estado = db.Column(db.String(20), default="activo")  # activo, devuelto, vencido
    
    # Relaciones
    usuario = db.relationship('Usuario', backref='prestamos')
    libro = db.relationship('Libro', backref='prestamos')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.fecha_devolucion_prevista:
            self.fecha_devolucion_prevista = datetime.utcnow() + timedelta(days=15)
    
    def marcar_devuelto(self):
        self.fecha_devolucion_real = datetime.utcnow()
        self.estado = "devuelto"
        if self.libro:
            self.libro.devolver()
    
    def calcular_mora(self):
        if self.estado == "activo" and datetime.utcnow() > self.fecha_devolucion_prevista:
            dias_retraso = (datetime.utcnow() - self.fecha_devolucion_prevista).days
            return max(0, dias_retraso)
        elif self.estado == "devuelto" and self.fecha_devolucion_real > self.fecha_devolucion_prevista:
            dias_retraso = (self.fecha_devolucion_real - self.fecha_devolucion_prevista).days
            return max(0, dias_retraso)
        return 0
    
    def esta_vencido(self):
        return self.estado == "activo" and datetime.utcnow() > self.fecha_devolucion_prevista
    
    def __str__(self):
        estado_str = self.estado
        if self.esta_vencido():
            estado_str = "vencido"
        return f'Préstamo: {self.usuario.nombre if self.usuario else "N/A"} - {self.libro.titulo if self.libro else "N/A"} - {estado_str}'
    
    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'libro_isbn': self.libro_isbn,
            'fecha_prestamo': self.fecha_prestamo.isoformat() if self.fecha_prestamo else None,
            'fecha_devolucion_prevista': self.fecha_devolucion_prevista.isoformat() if self.fecha_devolucion_prevista else None,
            'fecha_devolucion_real': self.fecha_devolucion_real.isoformat() if self.fecha_devolucion_real else None,
            'estado': self.estado,
            'dias_mora': self.calcular_mora()
        }