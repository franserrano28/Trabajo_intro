from flask import Flask
from flask_cors import CORS
from db.jugadores import get_all_players
app = Flask(__name__)

CORS(app)

@app.route('/players')
def hello_world():
    return get_all_players()

if __name__ == '__main__':
    app.run(port=8000)

   
