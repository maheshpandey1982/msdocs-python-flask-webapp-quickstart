import os
import pyodbc
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

basedir = os.path.abspath(os.path.dirname(__file__))

### database connectioon
server = 'azure-demo-server.database.windows.net'
database = 'azure_demo_db'
username = 'dainguyen'
password = 'dainn@13062002'
print("connecting.......")
cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = cnxn.cursor()
print("connected!")

app = Flask(__name__)

# Register blueprints here
from routes import bp as main_bp

app.register_blueprint(main_bp)

from routes import bp_emp, bp_ctm, bp_prod, bp_inv

app.register_blueprint(bp_emp, url_prefix='/employees')
app.register_blueprint(bp_ctm, url_prefix='/customers')
app.register_blueprint(bp_prod, url_prefix='/products')
app.register_blueprint(bp_inv, url_prefix='/invoices')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')

    if name:
        print('Request for hello page received with name=%s' % name)
        return render_template('hello.html', name=name)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
