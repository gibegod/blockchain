from flask import Flask, render_template, request, redirect, url_for, abort, flash, jsonify
from flask_cors import CORS
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse
from forms import SignupForm, LoginForm, ContractForm, WalletForm
import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from deployContract import newContract, movementHash, w3 #contractAccount

app = Flask(__name__, static_folder = "./fronted/dist/static", template_folder = "./fronted/dist")
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/mercadoblockchain'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

login_manager = LoginManager(app)
login_manager.login_view = "login" #en caso de que no este identidicado, y la vista lo requiera te manda para aca
db = SQLAlchemy(app)

from models import User, Contract, Wallet

@app.route('/', defaults={'path': ''})

#@app.route('/')
#def dender_vue():
#    return login();

@app.route("/")
def index():
    contracts = Contract.get_all()
    return render_template("index.html", contracts=contracts)


@app.route("/account")
@login_required #añado en varios lugares el login_required, osea que es necesario estas registrado para que entren a estas rutas
def account():
    return render_template("myaccount.html")


@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    form = SignupForm(request.form)
    if request.method == 'POST':
        if form.validate():
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user is None:
                # Creamos el usuario y lo guardamos
                user = User(name=name, email=email)
                user.set_password(password)
                user.save()
                # Dejamos al usuario logueado
                login_user(user, remember=True)
                return redirect(url_for('account'))
            flash('A user already exists with that email address.')
            return redirect(url_for('show_signup_form'))
    return render_template("signup_form.html", form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user:
                if user.check_password(password=password):
                    login_user(user)
                    next = request.args.get('next')
                    return redirect(next or url_for('account'))
        flash('Invalid username/password combination')
        return redirect(url_for('login'))
    return render_template('login_form.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


#formulario para crear los contratos, tambien muestra los existentes
@app.route("/contract", methods=['GET','POST']) #defaults={'contract_id': None}
#@app.route("/contract/<int: contract_id>")
@login_required
def contract():
    contracts = Contract.get_by_idowner(current_user.id) #traigo todos los contratos del que este usuario es dueño
    form = ContractForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        price = form.price.data
        contract_address = newContract(title, price) #inicio contrato y creo en la base de datos
        contract = Contract(owner_id= current_user.id, address = contract_address, title = title, description = description, price = price)
        contract.save()
        return redirect(url_for('index'))
    return render_template('contract.html', contracts=contracts, form=form)


@app.route("/new" , methods=['GET','POST'])
@login_required
def new():
    return render_template('contract.html') 