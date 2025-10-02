from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

class Reserva:
    def __init__(self, usuario, libro, fecha_reserva: Optional[datetime] = None,
                 id: Optional[str] = None):
        self.id = id or str(uuid4())
        self.usuario = usuario
        self.libro = libro
        self.fecha_reserva = fecha_reserva or datetime.now()
        self.fecha_expiracion = self.fecha_reserva + timedelta(days=3)  # 3 días de reserva
        self.estado = 'activa'  # 'activa', 'expirada', 'cancelada', 'completada'

    def activar_reserva(self) -> bool:
        """Activa la reserva si el libro está disponible"""
        if self.libro.esta_disponible() and self.estado == 'activa':
            self.estado = 'completada'
            return True
        return False

    def cancelar_reserva(self):
        """Cancela la reserva"""
        self.estado = 'cancelada'

    def verificar_expiracion(self):
        """Verifica si la reserva ha expirado"""
        if (self.estado == 'activa' and 
            datetime.now() > self.fecha_expiracion):
            self.estado = 'expirada'

    def esta_activa(self) -> bool:
        """Verifica si la reserva está activa"""
        self.verificar_expiracion()
        return self.estado == 'activa'

    def to_dict(self) -> dict:
        """Convierte el objeto a diccionario para serialización"""
        return {
            'id': self.id,
            'usuario_id': self.usuario.id,
            'libro_id': self.libro.id,
            'fecha_reserva': self.fecha_reserva.isoformat(),
            'fecha_expiracion': self.fecha_expiracion.isoformat(),
            'estado': self.estado
        }

    @classmethod
    def from_dict(cls, data: dict, usuario, libro):
        """Crea un objeto Reserva desde un diccionario"""
        reserva = cls(
            usuario=usuario,
            libro=libro,
            fecha_reserva=datetime.fromisoformat(data['fecha_reserva']),
            id=data.get('id')
        )
        
        reserva.fecha_expiracion = datetime.fromisoformat(data['fecha_expiracion'])
        reserva.estado = data['estado']
        
        return reserva