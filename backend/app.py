from flask import Flask

app = Flask(__name__)
app.secret_key = "Secret Key"
DATABASE_URI = \
    'mysql+pymysql://{user}:{password}@{server}/{database}'\
        .format(user='root', password='', server='localhost', database='aspmarks')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = 'static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
