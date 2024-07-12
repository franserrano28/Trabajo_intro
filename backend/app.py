from flask import Flask, request, jsonify
from models import db, Equipo, Jugador, Partido, Equipo_rivales


from flask_cors import CORS

app = Flask(__name__)
port = 5000
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgresql:postgresql@localhost:5432/marteeen'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello world!'


@app.route('/jugadores', methods=['GET'])
def get_jugadores():
    try:
        jugadores = Jugador.query.all()
        jugadores_data = []
        for jugador in jugadores:
            jugador_data = {
                'id': jugador.id,
                'nombre': jugador.nombre_jugador,
                'posicion': jugador.posicion,
                'nacionalidad': jugador.nacionalidad,
                'edad': jugador.edad,
                'puntaje': jugador.puntaje
            }
            jugadores_data.append(jugador_data)
        return jsonify(jugadores_data)
    except Exception as e:
        return jsonify({'error': 'Internal server error'})


@app.route('/equipos', methods=['GET'])
def get_equipos():
    try:
        equipos = Equipo.query.all()
        equipos_data = []
        for equipo in equipos:
            equipo_data = {
                'id': equipo.id,
                'nombre': equipo.nombre_equipo,
                'puntaje': equipo.puntaje,
                'fecha creacion': equipo.fecha_creacion,
                'arquero id': equipo.arquero_id,
                'defensor 1 id': equipo.defensa1_id,
                'defensor 2 id': equipo.defensa2_id,
                'mediocampista id': equipo.medio_id,
                'delantero id': equipo.delantero_id,
            }
            equipos_data.append(equipo_data)
        return jsonify(equipos_data)
    except Exception as e:
        return jsonify({'error': 'Internal server error'})


@app.route('/guardar_equipo', methods=['POST'])
def add_equipo():
    try:
        # Obtener datos del cuerpo de la solicitud JSON
        data = request.json

        # Extraer información del JSON recibido
        nombre_equipo = data.get('nombre_equipo')
        puntaje = data.get('puntaje')
        arquero_id = data.get('arquero_id')
        defensa1_id = data.get('defensa1_id')
        defensa2_id = data.get('defensa2_id')
        medio_id = data.get('medio_id')
        delantero_id = data.get('delantero_id')

        # Crear una nueva instancia del modelo Equipo
        nuevo_equipo = Equipo(
            nombre_equipo=nombre_equipo,
            puntaje=puntaje,
            arquero_id=arquero_id,
            defensa1_id=defensa1_id,
            defensa2_id=defensa2_id,
            medio_id=medio_id,
            delantero_id=delantero_id
        )

        # Añadir el nuevo equipo a la sesión de la base de datos
        db.session.add(nuevo_equipo)

        # Confirmar (commit) los cambios en la base de datos
        db.session.commit()

        # Devolver una respuesta con los detalles del equipo creado
        return jsonify({
            'equipo': {
                'id': nuevo_equipo.id,
                'nombre_equipo': nuevo_equipo.nombre_equipo,
                'puntaje': nuevo_equipo.puntaje,
                'fecha_creacion': nuevo_equipo.fecha_creacion,
                'arquero_id': nuevo_equipo.arquero_id,
                'defensa1_id': nuevo_equipo.defensa1_id,
                'defensa2_id': nuevo_equipo.defensa2_id,
                'medio_id': nuevo_equipo.medio_id,
                'delantero_id': nuevo_equipo.delantero_id
            }
        }), 201
    except Exception as error:
        # Manejar errores y devolver un mensaje de error
        print('Error:', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/eliminar_equipo/<int:equipo_id>', methods=['DELETE'])
def eliminar_equipo(equipo_id):
    try:
        equipo = Equipo.query.get_or_404(equipo_id)
        db.session.delete(equipo)
        db.session.commit()
        return jsonify({'message': 'Equipo eliminado correctamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'No se pudo eliminar el equipo', 'message': str(e)}), 500


@app.route('/equipos/<int:equipo_id>', methods=['PUT'])
def editar_equipo(equipo_id):
    try:
        data = request.json
        equipo = Equipo.query.get_or_404(equipo_id)

        # Actualizar datos del equipo
        equipo.nombre_equipo = data.get('nombre_equipo', equipo.nombre_equipo)
        equipo.puntaje = data.get('puntaje', equipo.puntaje)
        # Actualizar jugadores asociados si es necesario
        equipo.arquero_id = data.get('arquero_id', equipo.arquero_id)
        equipo.defensa1_id = data.get('defensa1_id', equipo.defensa1_id)
        equipo.defensa2_id = data.get('defensa2_id', equipo.defensa2_id)
        equipo.medio_id = data.get('medio_id', equipo.medio_id)
        equipo.delantero_id = data.get('delantero_id', equipo.delantero_id)

        db.session.commit()

        return jsonify({'message': 'Equipo actualizado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print('Starting server...')
    with app.app_context():
        db.create_all()
    print('Started...')
    app.run(host='0.0.0.0', debug=True, port=port)
