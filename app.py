import sys
from flask import Flask, request
from keras.models import load_model
from utils import rmsle, make_pass_token


app = Flask(__name__)


def predict(x: str) -> float:
    model = load_model('models/lstm_32emb_63d.h5', custom_objects={'rmsle': rmsle}, compile=False)
    y_pred = model.predict(make_pass_token(x), batch_size=1)
    return y_pred[0][0]


@app.before_first_request
def initialize():
    print("Called only once, when the first request comes in")



@app.route("/password", methods=['GET'])
def main():
    pw = request.args.get('password')
    pass_len = predict(pw)
    return f'Frequency for password "{pw}": {pass_len:.3f}'


if __name__ == '__main__':
    app.run(debug=True, threaded=False)


