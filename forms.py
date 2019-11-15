
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()]) #se podria agregar lo de repetir la contraseña
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrar')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()]) 
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')

class ContractForm(FlaskForm): #creo formulario de contrato
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField('Description')
    price = StringField('Precio', validators=[DataRequired()])
    submit = SubmitField('Crear contrato')


class WalletForm(FlaskForm): #formulario de billetera
    name = StringField('Título', validators=[DataRequired(), Length(max=128)])
    content = TextAreaField('Contenido', validators =[DataRequired()])
    submit = SubmitField('Conectar billetera')
