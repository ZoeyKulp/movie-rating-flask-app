from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

from assets_data_prep import prepare_data


app = Flask(__name__)

MODEL_PATH = "trained_model.pkl"

# Load the trained model once when the server starts
model = joblib.load(MODEL_PATH)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # 1. Read JSON data from the HTML form
        data = request.get_json()

        if data is None:
            return jsonify({
                "error": "No input data received"
            }), 400

        # 2. Required raw input fields
        required_fields = [
            "startYear",
            "runtimeMinutes",
            "genres",
            "Language",
            "Country"
        ]

        # 3. Check missing fields
        missing_fields = [
            field for field in required_fields
            if field not in data or str(data[field]).strip() == ""
        ]

        if missing_fields:
            return jsonify({
                "error": "Missing required field(s): " + ", ".join(missing_fields)
            }), 400

        # 4. Validate numeric fields
        try:
            data["startYear"] = int(data["startYear"])
            data["runtimeMinutes"] = float(data["runtimeMinutes"])
        except ValueError:
            return jsonify({
                "error": "startYear and runtimeMinutes must be numeric values"
            }), 400

        # 5. Validate text fields
        text_fields = ["genres", "Language", "Country"]

        for field in text_fields:
            if str(data[field]).strip().isdigit():
                return jsonify({
                    "error": f"{field} must be a text value"
                }), 400

        # 6. Build one-row DataFrame
        input_df = pd.DataFrame([data])

        # 7. Apply prepare_data
        processed_df = prepare_data(input_df)

        # Convert columns to float for model prediction
        processed_df = processed_df.astype(float)


        # 8. Predict rating
        prediction = model.predict(processed_df)[0]

        # 9. Return result
        return jsonify({
            "predicted_rating": round(float(prediction), 2)
        })

    except Exception:
        return jsonify({
        "error": "Internal server error"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)