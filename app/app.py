import os
import toml

from flask import Flask, request, jsonify, render_template
from lstm_model.base_model import PasswordLSTM
from lstm_model.utils import response_json

# Flask instance
app = Flask(__name__)
config = toml.load("config.toml")
# TODO: model_folder should be in config
model_folder = "model"

# Model class instance
password_model = PasswordLSTM(
    config=config,
    model_serialized=os.path.join(model_folder, "one_epoch_model"),
    tokenizer=os.path.join(model_folder, "tokenizer.pickle"),
)


@app.route("/", methods=["POST", "GET"])
def index():
    """Main form rendering"""
    if request.method == "POST":
        action = request.form["action"] == "predict"
        pw = request.form["password"]
        pass_freq = password_model.predict(pw)
        return render_template("index.html", password=pw, prediction=pass_freq)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    # for development set "debug=True" in app.run
    app.run(host="0.0.0.0", threaded=False, debug=True)
