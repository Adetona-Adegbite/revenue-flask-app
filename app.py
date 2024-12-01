from flask import Flask, request, jsonify
from joblib import load
import pandas as pd
from supabase import create_client, Client
import datetime

app = Flask(__name__)

model = load("traffic_model.pkl")

connection_string = "https://qyndfzptnprhmwxkegrf.supabase.co"
supabase: Client = create_client(connection_string,"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF5bmRmenB0bnByaG13eGtlZ3JmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMwNjMwMzMsImV4cCI6MjA0ODYzOTAzM30.WLb3wTS-tKJp3GIWCy1q-NQD8gXV1zSe6pGs3LcopBg")


def store_prediction_data(packet_data, prediction):
    data = {
        "duration": packet_data['duration'],
        "protocol_type": packet_data['protocol_type'],
        "service": packet_data['service'],
        "flag": packet_data['flag'],
        "src_bytes": packet_data['src_bytes'],
        "dst_bytes": packet_data['dst_bytes'],
        "land": packet_data['land'],
        "wrong_fragment": packet_data['wrong_fragment'],
        "urgent": packet_data['urgent'],
        "hot": packet_data['hot'],
        "num_failed_logins": packet_data['num_failed_logins'],
        "logged_in": packet_data['logged_in'],
        "num_compromised": packet_data['num_compromised'],
        "root_shell": packet_data['root_shell'],
        "su_attempted": packet_data['su_attempted'],
        "num_root": packet_data['num_root'],
        "num_file_creations": packet_data['num_file_creations'],
        "num_shells": packet_data['num_shells'],
        "num_access_files": packet_data['num_access_files'],
        "num_outbound_cmds": packet_data['num_outbound_cmds'],
        "is_host_login": packet_data['is_host_login'],
        "is_guest_login": packet_data['is_guest_login'],
        "count": packet_data['count'],
        "srv_count": packet_data['srv_count'],
        "serror_rate": packet_data['serror_rate'],
        "srv_serror_rate": packet_data['srv_serror_rate'],
        "rerror_rate": packet_data['rerror_rate'],
        "srv_rerror_rate": packet_data['srv_rerror_rate'],
        "same_srv_rate": packet_data['same_srv_rate'],
        "diff_srv_rate": packet_data['diff_srv_rate'],
        "srv_diff_host_rate": packet_data['srv_diff_host_rate'],
        "dst_host_count": packet_data['dst_host_count'],
        "dst_host_srv_count": packet_data['dst_host_srv_count'],
        "dst_host_same_srv_rate": packet_data['dst_host_same_srv_rate'],
        "dst_host_diff_srv_rate": packet_data['dst_host_diff_srv_rate'],
        "dst_host_same_src_port_rate": packet_data['dst_host_same_src_port_rate'],
        "dst_host_srv_diff_host_rate": packet_data['dst_host_srv_diff_host_rate'],
        "dst_host_serror_rate": packet_data['dst_host_serror_rate'],
        "dst_host_srv_serror_rate": packet_data['dst_host_srv_serror_rate'],
        "dst_host_rerror_rate": packet_data['dst_host_rerror_rate'],
        "dst_host_srv_rerror_rate": packet_data['dst_host_srv_rerror_rate'],
        "prediction": prediction,
    }
    supabase.table('traffic_predictions').insert(data).execute()


@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = request.get_json()
        feature_df = pd.DataFrame([input_data])
        prediction = model.predict(feature_df)[0]
        store_prediction_data(input_data, prediction)
        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
