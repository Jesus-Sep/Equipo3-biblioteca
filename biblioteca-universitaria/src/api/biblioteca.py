from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from src.extensions import db
from src.models import Libro, Estudiante, Prestamo

# Crear blueprint para la biblioteca
biblioteca_bp = Blueprint('biblioteca', __name__)

@biblioteca_bp.route('/')
def index():
    """Endpoint raíz de la API"""
    return jsonify({
        'message': 'Bienvenido a la API de Biblioteca Universitaria',
        'version': '1.0.0',
        'endpoints': {
            'libros': '/api/libros',
            'estudiantes': '/api/estudiantes',
            'prestamos': '/api/prestamos'
        }
    })

# Endpoints para Libros
@biblioteca_bp.route('/libros', methods=['GET'])
def listar_libros():
    """Obtener todos los libros"""
    try:
        libros = Libro.query.all()
        return jsonify({
            'success': True,
            'data': [libro.to_dict() for libro in libros],
            'count': len(libros)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@biblioteca_bp.route('/libros/<int:libro_id>', methods=['GET'])
def obtener_libro(libro_id):
    """Obtener un libro específico por ID"""
    libro = Libro.query.get_or_404(libro_id)
    return jsonify({
        'success': True,
        'data': libro.to_dict()
    })

@biblioteca_bp.route('/libros', methods=['POST'])
def crear_libro():
    """Crear un nuevo libro"""
    try:
        data = request.get_json()
        
        # Validaciones básicas
        if not data.get('titulo') or not data.get('autor'):
            return jsonify({
                'success': False,
                'error': 'Título y autor son obligatorios'
            }), 400
        
        libro = Libro(
            titulo=data['titulo'],
            autor=data['autor'],
            isbn=data.get('isbn', ''),
            editorial=data.get('editorial', ''),
            año_publicacion=data.get('año_publicacion'),
            categoria=data.get('categoria', 'General'),
            ejemplares_totales=data.get('ejemplares_totales', 1),
            ejemplares_disponibles=data.get('ejemplares_disponibles', 1)
        )
        
        db.session.add(libro)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': libro.to_dict(),
            'message': 'Libro creado exitosamente'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error al crear libro: {str(e)}'
        }), 500

# Endpoints para Estudiantes
@biblioteca_bp.route('/estudiantes', methods=['GET'])
def listar_estudiantes():
    """Obtener todos los estudiantes"""
    try:
        estudiantes = Estudiante.query.all()
        return jsonify({
            'success': True,
            'data': [estudiante.to_dict() for estudiante in estudiantes],
            'count': len(estudiantes)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@biblioteca_bp.route('/estudiantes', methods=['POST'])
def crear_estudiante():
    """Crear un nuevo estudiante"""
    try:
        data = request.get_json()
        
        # Validaciones
        required_fields = ['codigo_estudiante', 'nombre', 'apellido', 'email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'El campo {field} es obligatorio'
                }), 400
        
        # Verificar si el código o email ya existen
        if Estudiante.query.filter_by(codigo_estudiante=data['codigo_estudiante']).first():
            return jsonify({
                'success': False,
                'error': 'Ya existe un estudiante con este código'
            }), 400
            
        if Estudiante.query.filter_by(email=data['email']).first():
            return jsonify({
                'success': False,
                'error': 'Ya existe un estudiante con este email'
            }), 400
        
        estudiante = Estudiante(
            codigo_estudiante=data['codigo_estudiante'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            email=data['email'],
            carrera=data.get('carrera', 'No especificada'),
            semestre=data.get('semestre')
        )
        
        db.session.add(estudiante)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': estudiante.to_dict(),
            'message': 'Estudiante creado exitosamente'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error al crear estudiante: {str(e)}'
        }), 500

# Endpoints para Préstamos
@biblioteca_bp.route('/prestamos', methods=['GET'])
def listar_prestamos():
    """Obtener todos los préstamos"""
    try:
        prestamos = Prestamo.query.all()
        return jsonify({
            'success': True,
            'data': [prestamo.to_dict() for prestamo in prestamos],
            'count': len(prestamos)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@biblioteca_bp.route('/prestamos', methods=['POST'])
def crear_prestamo():
    """Crear un nuevo préstamo"""
    try:
        data = request.get_json()
        
        libro = Libro.query.get_or_404(data['libro_id'])
        estudiante = Estudiante.query.get_or_404(data['estudiante_id'])
        
        # Verificar disponibilidad
        if libro.ejemplares_disponibles <= 0:
            return jsonify({
                'success': False,
                'error': 'No hay ejemplares disponibles de este libro'
            }), 400
        
        # Verificar si el estudiante ya tiene préstamos activos del mismo libro
        prestamo_activo = Prestamo.query.filter_by(
            libro_id=data['libro_id'],
            estudiante_id=data['estudiante_id'],
            estado='activo'
        ).first()
        
        if prestamo_activo:
            return jsonify({
                'success': False,
                'error': 'El estudiante ya tiene un préstamo activo de este libro'
            }), 400
        
        # Crear préstamo
        prestamo = Prestamo(
            libro_id=data['libro_id'],
            estudiante_id=data['estudiante_id'],
            fecha_devolucion_esperada=datetime.utcnow() + timedelta(days=15)
        )
        
        # Actualizar disponibilidad
        libro.ejemplares_disponibles -= 1
        
        db.session.add(prestamo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': prestamo.to_dict(),
            'message': 'Préstamo creado exitosamente'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error al crear préstamo: {str(e)}'
        }), 500

@biblioteca_bp.route('/prestamos/devolver/<int:prestamo_id>', methods=['POST'])
def devolver_libro(prestamo_id):
    """Registrar devolución de un libro"""
    try:
        prestamo = Prestamo.query.get_or_404(prestamo_id)
        libro = Libro.query.get(prestamo.libro_id)
        
        if prestamo.estado == 'devuelto':
            return jsonify({
                'success': False,
                'error': 'El libro ya fue devuelto anteriormente'
            }), 400
        
        prestamo.estado = 'devuelto'
        prestamo.fecha_devolucion_real = datetime.utcnow()
        libro.ejemplares_disponibles += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': prestamo.to_dict(),
            'message': 'Libro devuelto exitosamente'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Error al devolver libro: {str(e)}'
        }), 500