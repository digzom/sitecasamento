from datetime import datetime
from appcasorio import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from appcasorio import login

# classe user herdando de db.Model a capacidade de definir os campos instanciados, usando UserMixin para as
# propriedades de login
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # cria uma chave encriptada da senha para aumentar a segurança
    profile = db.Column(db.String(24), index=True)

    def __repr__(self):
        return f'<User {self.username}>'  # printando no terminal para deixar mais claro quem é o usuário

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    url = db.Column(db.String(500), index=True)
    aprovado = db.Column(db.Boolean, index=True)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))