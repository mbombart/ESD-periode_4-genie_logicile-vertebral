import os
import random

import joblib
import numpy as np
import yaml
from flask import Flask, jsonify, render_template, request

webapp_root = "webapp"
params_path = "params.yaml"

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def predict(data):
    config = read_params(params_path)
    model_dir_path = config["model_webapp_dir"]

    model = joblib.load(model_dir_path)

    prediction = model.predict(data).tolist()[0]

    return prediction


def form_response(dict_request):
    print(dict_request)
    data = dict_request.values()
    data = [list(map(float, data))]

    print("done form response")
    response = predict(data)
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            if request.form:
                dict_req = dict(request.form)

                response = form_response(dict_req)

                return render_template("index.html", response = response)
        except Exception as e:
            print(e)
            error = {"error": "Something went wrong!! Try again later!"}
            error = {"error": e}
            return render_template("404.html", error=error)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    port = 5000 + random.randint(0, 999)
    print(port)
    url = "http://127.0.0.1:{0}".format(port)
    print(url)
    app.run(use_reloader=False, debug=True, port=port)
