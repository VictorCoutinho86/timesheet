from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, IntegerField, TextAreaField,\
    FileField, DateTimeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Usuario


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Usuário', validators=[DataRequired()])
    pis = StringField('PIS', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cadastre-se')

    def validate_username(self, username):
        user = Usuario.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Escolha outro nome de usuário.')

    def validate_email(self, email):
        user = Usuario.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Este e-mail já está cadastrado.')

    def validate_pis(self, pis):
        user = Usuario.query.filter_by(pis=pis.data).first()
        if user is not None:
            raise ValidationError('Já existe um cadastro com este numero de PIS.')


class OcorrenciaForm(FlaskForm):
    colaborador = StringField('Colaborador', validators=[DataRequired()])
    data_ocorrencia = DateField('Data Ocorrência', validators=[DataRequired()], format='%d-%m-%Y')
    hora_inicio = IntegerField('Inicio da Ocorrência', validators=[DataRequired()])
    hora_fim = IntegerField('Final da Ocorrência', validators=[DataRequired()])
    justificativa = TextAreaField('Justificativa', validators=[DataRequired()])
    submit = SubmitField('Enviar')

    def validate_data_ocorrencia(self, colaborador, data_ocorrencia):
        user = Usuario.query.filter_by(colaborador=colaborador.data, data_ocorrencia=data_ocorrencia.data).first()
        if user is not None:
            raise ValidationError('Já foi incluida está justificativa.')


class RespostaForm(FlaskForm):
    resposta = StringField('Resposta')
    status = BooleanField('Aceito?', validators=[DataRequired()])
    gestor = StringField('Gestor', validators=[DataRequired()])
    submit = SubmitField('Enviar')


class IntegracaoForm(FlaskForm):
    arquivo = FileField('Arquivo', validators=[DataRequired()])
    colaborador = StringField('Colaborador', validators=[DataRequired()])
    submit = SubmitField('Enviar')

    def validate_arquivo(self, arquivo):
        if arquivo.data is None:
            raise ValidationError('Selecione um arquvio valido!')
