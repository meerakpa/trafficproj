from flask import Flask, request, jsonify
from google.cloud import bigquery

app = Flask(__name__)
client = bigquery.Client()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    query = f"""
        SELECT predicted_traffic_count
        FROM ML.PREDICT(
            MODEL `meerapdataset.traffic_predict_model`,
            (SELECT '{data['date']}' AS traffic_count_date, '{data['location']}' AS location)
        )
    """
    result = client.query(query).result()
    predictions = [dict(row) for row in result]
    return jsonify(predictions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
