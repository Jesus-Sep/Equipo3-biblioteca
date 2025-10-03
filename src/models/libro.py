class Libro:
    def __init__(self, isbn: str, titulo: str, autor: str, genero: str, 
                 anio_publicacion: int, editorial: str, ejemplares_totales: int = 1):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.anio_publicacion = anio_publicacion
        self.editorial = editorial
        self.ejemplares_totales = ejemplares_totales
        self.ejemplares_disponibles = ejemplares_totales
        self.disponible = ejemplares_totales > 0
    
    def prestar(self):
        if self.ejemplares_disponibles > 0:
            self.ejemplares_disponibles -= 1
            self.disponible = self.ejemplares_disponibles > 0
            return True
        return False
    
    def devolver(self):
        if self.ejemplares_disponibles < self.ejemplares_totales:
            self.ejemplares_disponibles += 1
            self.disponible = True
            return True
        return False
    
    def actualizar_ejemplares(self, cantidad: int):
        if cantidad >= 0:
            diferencia = cantidad - self.ejemplares_totales
            self.ejemplares_totales = cantidad
            self.ejemplares_disponibles += diferencia
            self.disponible = self.ejemplares_disponibles > 0
            return True
        return False
    
    def __str__(self):
        return f"Libro: {self.titulo} - {self.autor} ({self.anio_publicacion}) - Disponibles: {self.ejemplares_disponibles}/{self.ejemplares_totales}"
    
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