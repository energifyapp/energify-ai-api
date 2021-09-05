from flask import Flask
from models.model_back import PredictionNet
import requests
import json

app = Flask(__name__)

#load model weights
model_1 = PredictionNet(1, name = "rooms_1")
model_1.build((None, 1))
model_1.load_weights('./models/model_1.h5')

@app.route('/form')
def get():
    INFORMATION = {"consumption":92, "type": "condo"} # SAMPLE DATA, DELETE LATER
    return INFORMATION

@app.route('/response')
def prediction():
    data = requests.get("http://localhost:5000/form")
    data_txt = json.loads(data.text)
    forecast = []
    day = int(model_1.predict((1, data_txt['consumption']))[1])
    for n in range(5):
        forecast.append(day)
        prediction = model_1.predict((1, day))
        day = float(prediction[1] + prediction[0])
    return {"prediction": forecast}

if __name__ == "__main__":
    app.run(debug = True)
