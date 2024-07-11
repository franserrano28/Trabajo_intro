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

if __name__ == '__main__':
    print('Starting server...')
    with app.app_context():
        db.create_all()
    print('Started...')
    app.run(host='0.0.0.0', debug=True, port=port)