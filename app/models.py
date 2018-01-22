from app import db, login
import locale
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')


class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pis = db.Column(db.Integer, unique=True, index=True, required=True)
    nome = db.Column(db.String(64), index=True, unique=True, required=True)
    email = db.Column(db.String(120), index=True, unique=True, required=True)
    username = db.Column(db.String(120, index=True, unique=True, required=True))
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    perfil_colaborador = db.Column(db.String(15))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return Usuario.query.get(int(id))


class Ocorrencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    justificativa = db.Column(db.String(240), required=True)
    data_ocorrencia = db.Column(db.Datetime)
    hora_inicio = db.Column(db.Integer, required=True)
    hora_fim - db.Column(db.Integer, required=True)
    id_colaborador = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    timestamp = db.Column(db.Datetime, default=datetime.utcnow())


class Resposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    justificativa = db.Column(db.Integer, db.ForeignKey('ocorrencia.id'))
    resposta = db.Column(db.String(240))
    status = db.Column(db.Boolean)
    id_gestor = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    timestamp = db.Column(db.Datetime, default=datetime.utcnow())


class Integracao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caminho = db.Column(db.String(240))
    timestamp = db.Column(db.Datetime, default=datetime.utcnow())
    # data_hora_ultimo_registro = db.Column(db.Datetime)
    id_colaborador = db.Column(db.Integer, db.ForeignKey('usuario.id'))

