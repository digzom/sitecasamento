from flask_wtf import FlaskForm  # usando WTForms para criar a página de login
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField  # campos para preenchimento das credenciais
from wtforms.validators import DataRequired, ValidationError, EqualTo  # esse validator checa se o campo está vazio
from appcasorio.models import User

class LoginForm(FlaskForm):  # criando a classe para gerar os campos
    username = StringField("Usuário", validators=[DataRequired()])
    password = PasswordField("Senha", validators=[DataRequired()])
    remember_me = BooleanField("Lembrar-me")
    submit = SubmitField("Entrar")


class RegistrationForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField(
        'Repita a senha', validators=[DataRequired(), EqualTo('password')])
    profile = SelectField('Perfil', choices=['Padrinho/Madrinha', 'Pai/Mãe', 'Amigo(a)/Familiar'], validators=[DataRequired()], render_kw={"placeholder": "Fulano"})
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Esse nome de usuário já existe.')

