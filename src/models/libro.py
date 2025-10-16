from src.extensions import db

class Libro(db.Model):
    __tablename__ = "libros"
    
    isbn = db.Column(db.String(20), primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(50))
    anio_publicacion = db.Column(db.Integer)
    editorial = db.Column(db.String(100))
    ejemplares_totales = db.Column(db.Integer, default=1)
    ejemplares_disponibles = db.Column(db.Integer, default=1)
    
    @property
    def disponible(self):
        return self.ejemplares_disponibles > 0
    
    def prestar(self):
        if self.ejemplares_disponibles > 0:
            self.ejemplares_disponibles -= 1
            return True
        return False
    
    def devolver(self):
        if self.ejemplares_disponibles < self.ejemplares_totales:
            self.ejemplares_disponibles += 1
            return True
        return False
    
    def actualizar_ejemplares(self, cantidad: int):
        if cantidad >= 0:
            diferencia = cantidad - self.ejemplares_totales
            self.ejemplares_totales = cantidad
            self.ejemplares_disponibles += diferencia
            return True
        return False
    
    def __str__(self):
        return f'Libro: {self.titulo} - {self.autor} ({self.anio_publicacion}) - Disponibles: {self.ejemplares_disponibles}/{self.ejemplares_totales}'
    
    def to_dict(self):
        return {
            'isbn': self.isbn,
            'titulo': self.titulo,
            'autor': self.autor,
            'genero': self.genero,
            'anio_publicacion': self.anio_publicacion,
            'editorial': self.editorial,
            'ejemplares_totales': self.ejemplares_totales,
            'ejemplares_disponibles': self.ejemplares_disponibles,
            'disponible': self.disponible
        }