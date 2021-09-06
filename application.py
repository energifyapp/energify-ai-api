from flask import Flask, render_template, request, redirect, jsonify
from models.model_back import PredictionNet
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.orm
from cockroachdb.sqlalchemy import run_transaction

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)
sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)


class Predictions(db.Model):
    __tablename__ = 'predictions'
    id = db.Column('todo_id', db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    text = db.Column(db.String)
    price = db.Column(db.Integer)
    
    def __init__(self, name, text):
        self.name = name
        self.text = text
        self.price = 0.20

#load model weights
model_1 = PredictionNet(1, name = "rooms_1")
model_1.build((None, 1))
model_1.load_weights('./models/model_1.h5')

model_3 = PredictionNet(1, name = "rooms_3")
model_3.build((None, 1))
model_3.load_weights('./models/model_3.h5')

model_4 = PredictionNet(1, name = "rooms_4")
model_4.build((None, 1))
model_4.load_weights('./models/model_4.h5')

model_5 = PredictionNet(1, name = "rooms_5")
model_5.build((None, 1))
model_5.load_weights('./models/model_5.h5')

model_condo = PredictionNet(1, name = "condo")
model_condo.build((None, 1))
model_condo.load_weights('./models/model_condo.h5')


@app.route('/form', methods = ['POST'])
def get():
    #data_txt = json.loads(data.text)
    forecast = []
    house_type = request.form['type']
    house_type = house_type.lower()
    if house_type == "1 and 2 rooms":
        model = model_1
    elif house_type == "3 rooms":
        model = model_3
    elif house_type == "4 rooms":
        model = model_4
    elif house_type == "5 rooms":
        model = model_5
    elif house_type == "condominium":
        model = model_condo
    else:
        model = model_1
    day = int(model.predict((1, int(request.form['kwh'])))[1])
    for _ in range(5):
        forecast.append(day)
        prediction = model_1.predict((1, day))
        day = float(prediction[1] + prediction[0])
    def ca(session):
        session.add(Predictions(request.form['name'],str(forecast),request.form['price']))
    run_transaction(sessionmaker, ca)
    return 'sucess'

@app.route('/search/<id>')
def show_all(id):
    def callback(session):
        return session.query(Predictions).filter(Predictions.name == id).first()
    return run_transaction(sessionmaker, callback)
    
    
if __name__ == "__main__":
    app.run(debug = True)
