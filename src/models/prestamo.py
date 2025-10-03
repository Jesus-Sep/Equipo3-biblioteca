import uuid
from datetime import datetime, timedelta

class Prestamo:
    def __init__(self, usuario, libro, dias_prestamo: int = 15):
        self.id = str(uuid.uuid4())
        self.usuario = usuario
        self.libro = libro
        self.fecha_prestamo = datetime.now()
        self.fecha_devolucion_prevista = self.fecha_prestamo + timedelta(days=dias_prestamo)
        self.fecha_devolucion_real = None
        self.estado = "activo"  # activo, devuelto, vencido
    
    def marcar_devuelto(self):
        self.fecha_devolucion_real = datetime.now()
        self.estado = "devuelto"
        self.libro.devolver()
    
    def calcular_mora(self):
        if self.estado == "activo" and datetime.now() > self.fecha_devolucion_prevista:
            dias_retraso = (datetime.now() - self.fecha_devolucion_prevista).days
            return max(0, dias_retraso)
        elif self.estado == "devuelto" and self.fecha_devolucion_real > self.fecha_devolucion_prevista:
            dias_retraso = (self.fecha_devolucion_real - self.fecha_devolucion_prevista).days
            return max(0, dias_retraso)
        return 0
    
    def esta_vencido(self):
        return self.estado == "activo" and datetime.now() > self.fecha_devolucion_prevista
    
    def __str__(self):
        estado_str = self.estado
        if self.esta_vencido():
            estado_str = "vencido"
        
        return f"Préstamo: {self.usuario.nombre} - {self.libro.titulo} - {estado_str}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario.id,
            'libro_isbn': self.libro.isbn,
            'fecha_prestamo': self.fecha_prestamo.isoformat(),
            'fecha_devolucion_prevista': self.fecha_devolucion_prevista.isoformat(),
            'fecha_devolucion_real': self.fecha_devolucion_real.isoformat() if self.fecha_devolucion_real else None,
            'estado': self.estado,
            'dias_mora': self.calcular_mora()
        }