from flask import Flask, request, jsonify, render_template
from datetime import datetime
import os
from lstm_model.base_model import PasswordLSTM


# Flask instance
app = Flask(__name__)


# Model class instance
password_model = PasswordLSTM(
    model_serialized="one_epoch_model", tokenizer="tokenizer.pickle"
)



def response_json(pass_len: float):
    """Response formatting as json"""
    res = jsonify(
        {
            "status": "success",
            "prediction": f"{pass_len:.1f}",
            "upload_time": datetime.now(),
        }
    )
    return res


@app.route("/")
def index():
    """Main form rendering"""
    return render_template("index.html")


@app.route("/predict", methods=["GET"])
def main():
    """Request for prediction processing"""
    pw = request.args.get("password")
    pass_len = password_model.predict(pw)
    res = response_json(pass_len)
    return res


@app.route("/predict_press_button", methods=["POST"])
def press_predict():
    """Processing button press"""
    action = request.form["action"] == "predict"
    pw = request.form["password"]
    pass_len = password_model.predict(pw)
    res = response_json(pass_len)
    return res

if __name__ == "__main__":
    # for development set "debug=True"in app.run
    app.run(host="0.0.0.0", threaded=False)
