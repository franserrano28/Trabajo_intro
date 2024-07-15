import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from sqlalchemy.orm import relationship

class Equipo(db.Model):
    __tablename__ = 'equipos'
    id = db.Column(db.Integer, primary_key=True)
    nombre_equipo = db.Column(db.String(25), nullable=False)
    puntaje = db.Column(db.Integer, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.now)
    arquero_id = db.Column(db.Integer, db.ForeignKey('jugadores.id'))
    defensor_1_id = db.Column(db.Integer, db.ForeignKey('jugadores.id'))
    defensor_2_id = db.Column(db.Integer, db.ForeignKey('jugadores.id'))
    medio_id = db.Column(db.Integer, db.ForeignKey('jugadores.id'))
    delantero_id = db.Column(db.Integer, db.ForeignKey('jugadores.id'))


class Jugador(db.Model):
    __tablename__ = 'jugadores'
    id = db.Column(db.Integer, primary_key=True)
    nombre_jugador = db.Column(db.String(25), nullable=False)
    posicion = db.Column(db.String(3), nullable=False)
    nacionalidad = db.Column(db.String(20), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    puntaje = db.Column(db.Integer, nullable=False)


class Partido(db.Model):
    __tablename__ = 'partidos'
    id = db.Column(db.Integer, primary_key=True)
    equipo_local_id = db.Column(db.Integer, db.ForeignKey('equipos.id'))
    equipo_visitante_id = db.Column(db.Integer, db.ForeignKey('equipos.id'))
    resultado = db.Column(db.String(10), nullable=False)  # Cambiado a String para almacenar "2-1"
    goles_equipo_local = db.Column(db.Integer, nullable=False, default=0)
    goles_equipo_visitante = db.Column(db.Integer, nullable=False, default=0)
    fecha = db.Column(db.DateTime, default=datetime.datetime.now())





    

