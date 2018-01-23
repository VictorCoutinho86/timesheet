from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pis = db.Column(db.Integer, unique=True, index=True)
    nome = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    perfil_colaborador = db.Column(db.String(15))

    def __repr__(self):
        return '<Usuário {}>'.format(self.nome)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return Usuario.query.get(int(id))


class Ocorrencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    justificativa = db.Column(db.String(240))
    data_ocorrencia = db.Column(db.DateTime)
    hora_inicio = db.Column(db.Integer)
    hora_fim = db.Column(db.Integer)
    id_colaborador = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())


class Resposta(db.Model):
    justificativa = db.Column(db.Integer, db.ForeignKey('ocorrencia.id'), primary_key=True)
    resposta = db.Column(db.String(240))
    status = db.Column(db.Boolean)
    id_gestor = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())


class Integracao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caminho = db.Column(db.String(240))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    data_hora_ultimo_registro = db.Column(db.DateTime)
    id_colaborador = db.Column(db.Integer, db.ForeignKey('usuario.id'))

