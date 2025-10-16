from click import echo
from datetime import datetime, timedelta
from src.extensions import db
from src.models import Libro, Estudiante, Prestamo

def register_seed_command(app):
    @app.cli.command("seed")
    def seed():
        """Comando para poblar la base de datos con datos de ejemplo"""
        
        # Verificar si ya existen datos
        if Libro.query.first():
            echo("Seed already applied.")
            return

        # Crear libros de ejemplo
        libros = [
            Libro(
                titulo="Cien Años de Soledad",
                autor="Gabriel García Márquez",
                isbn="9788437604947",
                editorial="Sudamericana",
                año_publicacion=1967,
                categoria="Novela",
                ejemplares_totales=3,
                ejemplares_disponibles=3
            ),
            Libro(
                titulo="El Quijote de la Mancha",
                autor="Miguel de Cervantes",
                isbn="9788467031250",
                editorial="Editorial EDAF",
                año_publicacion=1605,
                categoria="Clásico",
                ejemplares_totales=2,
                ejemplares_disponibles=2
            ),
            Libro(
                titulo="Física Universitaria",
                autor="Sears & Zemansky",
                isbn="9786073220256",
                editorial="Pearson",
                año_publicacion=2013,
                categoria="Ciencia",
                ejemplares_totales=5,
                ejemplares_disponibles=5
            )
        ]
        
        # Crear estudiantes de ejemplo
        estudiantes = [
            Estudiante(
                codigo_estudiante="2023001",
                nombre="Ana",
                apellido="García",
                email="ana.garcia@universidad.edu",
                carrera="Ingeniería de Sistemas",
                semestre=5
            ),
            Estudiante(
                codigo_estudiante="2023002",
                nombre="Carlos",
                apellido="Rodríguez",
                email="carlos.rodriguez@universidad.edu",
                carrera="Literatura",
                semestre=3
            )
        ]
        
        # Agregar a la sesión
        for libro in libros:
            db.session.add(libro)
        for estudiante in estudiantes:
            db.session.add(estudiante)
        
        db.session.commit()
        
        echo("Seed completed. Created:")
        echo("- 3 libros")
        echo("- 2 estudiantes")