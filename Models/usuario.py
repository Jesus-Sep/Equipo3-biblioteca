import uuid
from datetime import datetime

class Usuario:
    def __init__(self, nombre: str, email: str, telefono: str = ""):
        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.activo = True
        self.fecha_registro = datetime.now()
    
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
            'fecha_registro': self.fecha_registro.isoformat()
        }