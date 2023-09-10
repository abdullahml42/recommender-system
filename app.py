import os
import secrets
import subprocess
import sys

from flask import Flask, jsonify, redirect, render_template, request, url_for

from recommender_system.pipeline import RecommendProducts

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route("/")
def index():
    """Renders the template for the home page."""
    return render_template("index.html")


@app.route("/train")
def train():
    """Triggers the training process."""
    venv_activate_script = get_activate_script()
    subprocess.call([venv_activate_script, "&&", "python", "main.py"], shell=True)
    return redirect(url_for("index"))


@app.route("/recommend", methods=["POST"])
def recommend():
    """Generates recommendations based on provided reviewer ID and number of items."""
    reviewer_id = request.json["reviewerId"]
    num_items = int(request.json["numItems"])
    recommendation_system = RecommendProducts(reviewer_id)
    recommendations = recommendation_system.recommend_products(num_items)
    return jsonify({"recommendations": recommendations.to_dict("records")})


def get_activate_script():
    """Returns the path to the virtual environment's activate script."""
    if sys.platform.startswith("win"):
        return os.path.join(os.environ.get("VIRTUAL_ENV"), "Scripts", "activate.bat")
    else:
        return os.path.join(os.environ.get("VIRTUAL_ENV"), "bin", "activate")


if __name__ == "__main__":
    app.run(debug=False, port=8000)
