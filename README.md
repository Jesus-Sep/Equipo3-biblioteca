classDiagram
    class Usuario {
        -String id
        -String nombre
        -String email
        -String tipo
        -Boolean activo
        -DateTime fecha_registro
        +prestamos_activos()
        +historial_prestamos()
        +puede_solicitar_prestamo()
    }

    class Libro {
        -String isbn
        -String titulo
        -String autor
        -String editorial
        -Integer año_publicacion
        -String categoria
        -Integer ejemplares_totales
        -Integer ejemplares_disponibles
        -String ubicacion
        -Boolean disponible
        +actualizar_disponibilidad()
        +buscar_por_criterio()
    }

    class Prestamo {
        -String id
        -Usuario usuario
        -Libro libro
        -DateTime fecha_prestamo
        -DateTime fecha_devolucion_prevista
        -DateTime fecha_devolucion_real
        -String estado
        -Integer renovaciones
        +calcular_mora()
        +renovar()
        +marcar_devuelto()
    }

    class Reserva {
        -String id
        -Usuario usuario
        -Libro libro
        -DateTime fecha_reserva
        -DateTime fecha_expiracion
        -String estado
        +activar_reserva()
        +cancelar_reserva()
    }

    Usuario "1" -- "*" Prestamo : realiza
    Libro "1" -- "*" Prestamo : prestado_en
    Usuario "1" -- "*" Reserva : realiza
    Libro "1" -- "*" Reserva : reservado_en