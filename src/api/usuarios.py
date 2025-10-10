"""
Blueprint para gestión de usuarios de la biblioteca universitaria.
Maneja operaciones relacionadas con estudiantes, profesores y personal.
"""

from flask import Blueprint, jsonify, request

usuarios_bp = Blueprint('usuarios', __name__)

# Datos de ejemplo
usuarios = [
    {
        'id': 1,
        'nombre': 'Ana García',
        'email': 'ana.garcia@universidad.edu',
        'tipo': 'estudiante',
        'carrera': 'Ingeniería Informática',
        'activo': True
    },
    {
        'id': 2,
        'nombre': 'Dr. Carlos López',
        'email': 'carlos.lopez@universidad.edu',
        'tipo': 'profesor',
        'departamento': 'Ciencias de la Computación',
        'activo': True
    }
]


@usuarios_bp.route('/', methods=['GET'])
def obtener_usuarios():
    """
    Obtiene todos los usuarios registrados.
    
    Returns:
        JSON: Lista de usuarios
    """
    return jsonify({
        'usuarios': usuarios,
        'total': len(usuarios)
    })


@usuarios_bp.route('/<int:usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    """
    Obtiene un usuario específico por su ID.
    
    Args:
        usuario_id: ID del usuario
        
    Returns:
        JSON: Datos del usuario
    """
    usuario = next((u for u in usuarios if u['id'] == usuario_id), None)
    
    if usuario is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    return jsonify({'usuario': usuario})


@usuarios_bp.route('/', methods=['POST'])
def crear_usuario():
    """
    Registra un nuevo usuario en el sistema.
    
    Returns:
        JSON: Datos del usuario creado
    """
    data = request.get_json()
    
    required_fields = ['nombre', 'email', 'tipo']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Datos incompletos'}), 400
    
    # Verificar si el email ya existe
    if any(u['email'] == data['email'] for u in usuarios):
        return jsonify({'error': 'El email ya está registrado'}), 400
    
    nuevo_usuario = {
        'id': len(usuarios) + 1,
        'nombre': data['nombre'],
        'email': data['email'],
        'tipo': data['tipo'],
        'activo': True
    }
    
    # Campos específicos por tipo de usuario
    if data['tipo'] == 'estudiante':
        nuevo_usuario['carrera'] = data.get('carrera', 'No especificada')
    elif data['tipo'] == 'profesor':
        nuevo_usuario['departamento'] = data.get('departamento', 'No especificado')
    
    usuarios.append(nuevo_usuario)
    
    return jsonify({
        'message': 'Usuario registrado exitosamente',
        'usuario': nuevo_usuario
    }), 201