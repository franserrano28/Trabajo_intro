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
        jugadores = Jugador.query.all() #trae todos los jugadores
        jugadores_data = [] #arma lista
        for jugador in jugadores:
            jugador_data = {
                'id': jugador.id,
                'nombre': jugador.nombre_jugador,
                'posicion': jugador.posicion,
                'nacionalidad': jugador.nacionalidad,
                'edad': jugador.edad,
                'puntaje': jugador.puntaje
            }
            jugadores_data.append(jugador_data) #agrega el diccionario del jugador a la lista
        return jsonify(jugadores_data) #te lo convierte en json

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
                'nombre_equipo': equipo.nombre_equipo,
                'puntaje': equipo.puntaje,
                'fecha_creacion': equipo.fecha_creacion,
                'arquero_id': equipo.arquero_id,
                'defensor_1_id': equipo.defensor_1_id,
                'defensor_2_id': equipo.defensor_2_id,
                'mediocampista_id': equipo.medio_id,
                'delantero_id': equipo.delantero_id,
            }
            equipos_data.append(equipo_data)
        return jsonify(equipos_data)
    except Exception as e:
        return jsonify({'error': 'Internal server error'})


@app.route('/equipos/<id_equipos>', methods=['GET'])
def get_equipo(id_equipos):
    try:
        equipo = Equipo.query.get(id_equipos)  # Obtener un equipo por su ID
        if equipo is None:
            return jsonify({'error': 'Equipo not found'}), 404

        equipo_data = {
                'id': equipo.id,
                'nombre_equipo': equipo.nombre_equipo,
                'puntaje': equipo.puntaje,
                'fecha_creacion': equipo.fecha_creacion,
                'arquero_id': equipo.arquero_id,
                'defensor_1_id': equipo.defensor_1_id,
                'defensor_2_id': equipo.defensor_2_id,
                'mediocampista_id': equipo.medio_id,
                'delantero_id': equipo.delantero_id,
            }
        return jsonify(equipo_data)
    except Exception as e:
        print(traceback.format_exc())  # Imprimir el error completo en la consola
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/guardar_equipo', methods=['POST'])
def nuevo_equipo():
    try:
        data = request.json # Obtener datos del cuerpo de la solicitud JSON

        # Extraer información del JSON recibido
        nombre_equipo = data.get('nombre_equipo')
        puntaje = data.get('puntaje')
        arquero_id = data.get('arquero_id')
        defensor_1_id = data.get('defensor_1_id')
        defensor_2_id = data.get('defensor_2_id')
        medio_id = data.get('medio_id')
        delantero_id = data.get('delantero_id')

        # Crear una nueva instancia del modelo Equipo
        nuevo_equipo = Equipo(
            nombre_equipo=nombre_equipo,
            puntaje=puntaje,
            arquero_id=arquero_id,
            defensor_1_id=defensor_1_id,
            defensor_2_id=defensor_2_id,
            medio_id=medio_id,
            delantero_id=delantero_id
        )

        db.session.add(nuevo_equipo) # Añadir el nuevo equipo a la sesión de la base de datos
        db.session.commit()# Confirmar (commit) los cambios en la base de datos

        # Devolver una respuesta con los detalles del equipo creado
        return jsonify({
            'equipo': {
                'id': nuevo_equipo.id,
                'nombre_equipo': nuevo_equipo.nombre_equipo,
                'puntaje': nuevo_equipo.puntaje,
                'fecha_creacion': nuevo_equipo.fecha_creacion,
                'arquero_id': nuevo_equipo.arquero_id,
                'defensor_1_id': nuevo_equipo.defensor_1_id,
                'defensor_2_id': nuevo_equipo.defensor_2_id,
                'medio_id': nuevo_equipo.medio_id,
                'delantero_id': nuevo_equipo.delantero_id
            }
        }), 201
    except Exception as error:
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/equipos/<equipo_id>', methods=['PUT'])
def editar_equipo(equipo_id):
    try:
        data = request.json # Obtener los datos JSON enviados en la solicitud
        equipo = Equipo.query.get_or_404(equipo_id) # Obtener el equipo por su ID o devolver un error 404 si no existe

        # Actualizar datos del equipo con los valores recibidos o mantener los actuales si no se proporcionan nuevos valores
        equipo.nombre_equipo = data.get('nombre_equipo', equipo.nombre_equipo)
        equipo.puntaje = data.get('puntaje', equipo.puntaje)
        equipo.arquero_id = data.get('arquero_id', equipo.arquero_id)
        equipo.defensor_1_id = data.get('defensor_1_id', equipo.defensor_1_id)
        equipo.defensor_2_id = data.get('defensor_2_id', equipo.defensor_2_id)
        equipo.medio_id = data.get('mediocampista_id', equipo.medio_id)
        equipo.delantero_id = data.get('delantero_id', equipo.delantero_id)

        db.session.commit() # Confirmar los cambios en la base de datos

        return jsonify({'message': 'Equipo actualizado correctamente'}), 200 # Devolver mensaje de éxito con código HTTP 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 # Devolver mensaje de error con código HTTP 500 en caso de excepción


@app.route('/eliminar_equipo/<equipo_id>', methods=['DELETE'])
def eliminar_equipo(equipo_id):
    try:
        equipo = Equipo.query.get_or_404(equipo_id) # Intenta obtener el equipo con el ID proporcionado o devuelve un error 404 si no existe
        db.session.delete(equipo)  # Elimina el equipo de la sesión de la base de datos
        db.session.commit()  # Confirma los cambios en la base de datos
        return jsonify({'message': 'Equipo eliminado correctamente'}), 200
    except Exception as e:
        db.session.rollback() # En caso de error, realiza un rollback para deshacer los cambios pendientes en la sesión de la base de datos
        return jsonify({'error': 'No se pudo eliminar el equipo', 'message': str(e)}), 500 # Devuelve una respuesta JSON indicando que no se pudo eliminar el equipo y el mensaje de error específico


if __name__ == '__main__':
    print('Starting server...')
    with app.app_context():
        db.create_all()
    print('Started...')
    app.run(host='0.0.0.0', debug=True, port=port)