from flask import Flask, request, jsonify
from joblib import load
import pandas as pd
import numpy as np

app = Flask(__name__)

model = load('Model.pkl')
@app.route("/predict", methods=["POST"])
def predict_rev():
    try:
        input_data = request.get_json()
        feature_df = pd.DataFrame([input_data])
        print("Input Data:", feature_df)

        results = []

        change_steps = np.linspace(-1, 1, 10)

        for i in range(10):
            num_changes = np.random.randint(1, len(feature_df.columns) + 1)  # Random number of features to modify
            modified_columns = np.random.choice(feature_df.columns, size=num_changes, replace=False)

            modified_input = feature_df.copy()

            print(f"Run {i + 1}: Selected Columns to Modify: {modified_columns}")

            for column in modified_columns:
                step = np.random.choice(change_steps)

                modified_input[column] = modified_input[column] * (1 + step)

                print(f"Column: {column}, Step: {step}, Modified Value: {modified_input[column].values[0]}")

            prediction = model.predict(modified_input)[0]
            print(f"Predicted Revenue: {prediction}")

            result = {
                "modified_features": modified_columns.tolist(),
                "modified_values": modified_input[modified_columns].values.flatten().tolist(),
                "predicted_revenue": prediction
            }

            results.append(result)

        # Convert the results to a DataFrame for consistency
        results_df = pd.DataFrame(results)

        print("Predictions with Feature Changes:")
        print(results_df)

        # Return the results as JSON
        return jsonify(results_df.to_dict(orient="records"))

    except Exception as e:
        return jsonify({"error": str(e)}), 400
if __name__ == "__main__":
    app.run(debug=True)
