"""
Punto de entrada principal para la API de Gestión de Biblioteca Universitaria.
"""

from src import create_app
from src.config import config
import os

# Determinar el entorno
environment = os.environ.get('FLASK_ENV', 'default')

# Crear la aplicación
app = create_app(config[environment])

if __name__ == '__main__':
    app.run(
        host=os.environ.get('HOST', '0.0.0.0'),
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config['DEBUG']
    )