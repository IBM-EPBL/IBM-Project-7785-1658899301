import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "3vLaYb7_R2R7GNNYiHSWjXX_iYd2gIb5jFDr-yeM1Zup"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line


app = Flask(__name__)
model = joblib.load('power_prediction.sav')

@app.route('/')
def home():
    return render_template('intro.html')

@app.route('/loginpage')
def loginpage():
    return render_template('loginpage.html')

@app.route('/SignUp')
def SignUp():
    return render_template('SignUp.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/windapi',methods=['POST'])
def windapi():
    city=request.form.get('city')
    apikey="c21dd661f7aac9a7720fe4ced3317b0a"
    url="http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+apikey
    resp = requests.get(url)
    resp=resp.json()
    temp = str(resp["main"]["temp"]-273.15) +" °C"
    humid = str(resp["main"]["humidity"])+" %"
    pressure = str(resp["main"]["pressure"])+" mmHG"
    speed = str(resp["wind"]["speed"])+" m/s"
    return render_template('predict.html', temp=temp, humid=humid, pressure=pressure,speed=speed)   
@app.route('/y_predict',methods=['POST'])
def y_predict():
    val_X = [[float(X) for X in request.form.values()]]
    print(val_X)
   
    
    
    payload_scoring = {"input_data": [{"field": ["Theoretical_Power_Curve (KWh)", "WindSpeed(m/s)"], 
                "values": val_X}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/720028d7-8db4-457f-83e8-0d4983053e59/predictions?version=2022-11-16', json=payload_scoring,
                                     headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions =response_scoring.json()
    print(predictions)
    print('Final Prediction Result',predictions['predictions'][0]['values'][0][0])


    pred =response_scoring.json()
    print(pred)
    output = pred['predictions'][0]['values'][0][0]
    return render_template('predict.html', prediction_text='The energy predicted is {:.2f} KWh'.format(output))


if __name__ == "__main__":
    app.run(debug=False)
