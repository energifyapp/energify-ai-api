from flask import Flask, render_template, request, redirect, jsonify
from models.model_back import PredictionNet
import requests
import json

app = Flask(__name__)

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


@app.route('/form')
def get():
    INFORMATION = {"kwh":103, "type": "3 rooms"} # SAMPLE DATA, DELETE LATER
    return INFORMATION

@app.route('/response', methods = ['POST', 'GET'])
def prediction():
    data = requests.get("http://localhost:5000/form")
    data_txt = json.loads(data.text)
    forecast = []
    house_type = data_txt['type']
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
    day = int(model.predict((1, data_txt['kwh']))[1])
    for _ in range(5):
        forecast.append(day)
        prediction = model_1.predict((1, day))
        day = float(prediction[1] + prediction[0])
    return {"prediction": forecast, "model":str(model.name)}

if __name__ == "__main__":
    app.run(debug = True)
