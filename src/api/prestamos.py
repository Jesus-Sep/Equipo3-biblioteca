"""
Blueprint para gesti�n de pr�stamos de libros.
Maneja el proceso de pr�stamo, devoluci�n y seguimiento.
"""

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta

prestamos_bp = Blueprint('prestamos', __name__)

# Datos de ejemplo
prestamos = [
    {
        'id': 1,
        'libro_id': 1,
        'usuario_id': 1,
        'fecha_prestamo': '2024-01-15',
        'fecha_devolucion_estimada': '2024-01-30',
        'fecha_devolucion_real': None,
        'estado': 'activo'
    }
]


@prestamos_bp.route('/', methods=['GET'])
def obtener_prestamos():
    """
    Obtiene todos los pr�stamos del sistema.
    
    Query Params:
        estado: Filtrar por estado ('activo', 'devuelto', 'vencido')
        
    Returns:
        JSON: Lista de pr�stamos
    """
    estado = request.args.get('estado')
    
    if estado:
        prestamos_filtrados = [p for p in prestamos if p['estado'] == estado]
    else:
        prestamos_filtrados = prestamos
    
    return jsonify({
        'prestamos': prestamos_filtrados,
        'total': len(prestamos_filtrados)
    })


@prestamos_bp.route('/', methods=['POST'])
def crear_prestamo():
    """
    Crea un nuevo pr�stamo de libro.
    
    Returns:
        JSON: Datos del pr�stamo creado
    """
    data = request.get_json()
    
    if not data or not all(key in data for key in ['libro_id', 'usuario_id']):
        return jsonify({'error': 'Datos incompletos'}), 400
    
    # En una implementaci�n real, verificar�amos:
    # - Que el libro existe y tiene ejemplares disponibles
    # - Que el usuario existe y est� activo
    # - Que el usuario no excede el l�mite de pr�stamos
    
    nuevo_prestamo = {
        'id': len(prestamos) + 1,
        'libro_id': data['libro_id'],
        'usuario_id': data['usuario_id'],
        'fecha_prestamo': datetime.now().strftime('%Y-%m-%d'),
        'fecha_devolucion_estimada': (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
        'fecha_devolucion_real': None,
        'estado': 'activo'
    }
    
    prestamos.append(nuevo_prestamo)
    
    return jsonify({
        'message': 'Pr�stamo registrado exitosamente',
        'prestamo': nuevo_prestamo
    }), 201


@prestamos_bp.route('/<int:prestamo_id>/devolver', methods=['POST'])
def devolver_libro(prestamo_id):
    """
    Registra la devoluci�n de un libro prestado.
    
    Args:
        prestamo_id: ID del pr�stamo a devolver
        
    Returns:
        JSON: Confirmaci�n de devoluci�n
    """
    prestamo = next((p for p in prestamos if p['id'] == prestamo_id), None)
    
    if prestamo is None:
        return jsonify({'error': 'Pr�stamo no encontrado'}), 404
    
    if prestamo['estado'] == 'devuelto':
        return jsonify({'error': 'El libro ya fue devuelto'}), 400
    
    prestamo['fecha_devolucion_real'] = datetime.now().strftime('%Y-%m-%d')
    prestamo['estado'] = 'devuelto'
    
    # En una implementaci�n real, actualizar�amos la disponibilidad del libro
    
    return jsonify({
        'message': 'Libro devuelto exitosamente',
        'prestamo': prestamo
    })


@prestamos_bp.route('/usuario/<int:usuario_id>', methods=['GET'])
def obtener_prestamos_usuario(usuario_id):
    """
    Obtiene todos los pr�stamos de un usuario espec�fico.
    
    Args:
        usuario_id: ID del usuario
        
    Returns:
        JSON: Pr�stamos del usuario
    """
    prestamos_usuario = [p for p in prestamos if p['usuario_id'] == usuario_id]
    
    return jsonify({
        'prestamos': prestamos_usuario,
        'total': len(prestamos_usuario),
        'usuario_id': usuario_id
    })




