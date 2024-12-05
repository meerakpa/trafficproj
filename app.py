from flask import Flask, request, jsonify
from google.cloud import bigquery
import os

app = Flask(__name__)
os.environ["GOOGLE_CLOUD_PROJECT"] = "citric-gradient-439303-u3"
client = bigquery.Client()

@app.route('/')
def home():
    return "Traffic Prediction API is running!", 200

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    query = f"""
        SELECT *
        FROM ML.PREDICT(
            MODEL `meerapdataset.traffic_predict_model`,
            (SELECT 
                1 AS ID, 
                DATE('{data['date']}') AS traffic_count_date, 
                '{data['location']}' AS location)
        )
    """
    try:
        result = client.query(query).result()
        predictions = [dict(row) for row in result]
        return jsonify(predictions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
