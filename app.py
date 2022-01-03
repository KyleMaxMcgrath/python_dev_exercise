from re import search
from flask import Flask, request
from flask_cors import CORS

import pandas as pd

app = Flask(__name__)
cors = CORS(app, resources={r"/search/": {"origins": "*"}})

df = pd.read_csv("data/patient_tb.csv")

seen = set()
i = 0
while i < len(df):
    test = str(df.iloc[i]['MostRecentTestDate']) + str(df.iloc[i]['TestName']) + str(df.iloc[i]['PatientID'])
    if test not in seen:
        seen.add(test)
        i+=1
    else:
        df = df.drop(labels=i,axis=0)



@app.route('/search/', methods=['POST'])
def home():
    search_term = request.get_json(force=True)
    result = df.loc[df['PatientFirstName'] == search_term]
    return result.transpose().to_json()

app.run(host="127.0.0.1", port=5000)