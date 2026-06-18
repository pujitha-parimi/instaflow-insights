import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/insights")
def insights():
    dataset_name = "instagram_influencers"

    image_folder = os.path.join(
        app.static_folder,
        "images",
        dataset_name
    )

    images = []
    if os.path.exists(image_folder):
        images = [
            f for f in os.listdir(image_folder)
            if f.endswith(".png")
        ]

    return render_template(
        "insights.html",
        dataset_name=dataset_name,
        images=images
    )

if __name__ == "__main__":
    app.run(debug=True)
