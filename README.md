# login-blockchain
Pasos: 
1. Crear una base de datos en MySQL con el nombre 'mercadoblockchain'.
2. Modificar el run.py con tus datos (mysql+pqmysql://user:password@host/database).
3. Crear un ambiente e instalar los paquetes ejecutando el siguiente comando: pip install -r requierements.txt
4. Dentro de la consola escribir 'python3', y luego:
>>> from run import db

>>> db.create_all()
5. Ejecutar los siguientes comandos:
set "FLASK_APP=run.py"
set "FLASK_ENV=development"
6. Ejecutar 'flask run'.
7. Dirigirse a localhost:5000/login y la magia ocurrira.

Base de datos en local: 'mysql+pymysql://root:@localhost/mercadoblockchain'
Base de datos en PythonAnywhere: 'mysql+pymysql://gibegod:lopez999@gibegod.mysql.pythonanywhere-services.com/gibegod$miniblog'


npm install truffle
pip install web3