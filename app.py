from setup import *
from models import *
from blueprints.account import account
from blueprints.admin import admin
from blueprints.parent import parent
from flask import render_template

app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(parent, url_prefix='/parent')

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
