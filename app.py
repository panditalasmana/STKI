from flask import Flask, render_template, request
from models.search import search_laptop
import pandas as pd

app = Flask(__name__)

# =========================
# LOAD DATASET
# =========================

df = pd.read_csv("dataset/laptop_dataset.csv")

# =========================
# HOME PAGE
# =========================

@app.route("/", methods=["GET", "POST"])
def index():

    query = ""
    results = []

    # =========================
    # ALL PRODUCTS
    # =========================

    all_products = []

    for i, row in df.iterrows():

        all_products.append({

            "id": row["id"],

            "nama": row["nama_laptop"],

            "harga": f"Rp {row['harga']:,}".replace(",", "."),

            "deskripsi": row["deskripsi"]

        })

    # =========================
    # SEARCH
    # =========================

    if request.method == "POST":

        query = request.form["query"]

        results = search_laptop(query)

    # =========================
    # EVALUATION DATA
    # =========================

    evaluation_data = [

        {
            "query": "laptop gaming",
            "precision": 0.8
        },

        {
            "query": "laptop mahasiswa",
            "precision": 0.7
        },

        {
            "query": "laptop editing",
            "precision": 0.9
        },

        {
            "query": "laptop murah",
            "precision": 0.6
        },

        {
            "query": "laptop RTX",
            "precision": 0.9
        },

        {
            "query": "laptop office",
            "precision": 0.8
        },

        {
            "query": "laptop desain grafis",
            "precision": 0.8
        },

        {
            "query": "laptop tipis",
            "precision": 0.7
        },

        {
            "query": "laptop coding",
            "precision": 0.8
        },

        {
            "query": "laptop SSD",
            "precision": 0.9
        }

    ]

    # =========================
    # AVERAGE PRECISION
    # =========================

    average_precision = round(

        sum(
            item["precision"]
            for item in evaluation_data
        ) / len(evaluation_data),

        2

    )

    # =========================
    # RENDER
    # =========================

    return render_template(

        "index.html",

        results=results,

        query=query,

        all_products=all_products,

        evaluation_data=evaluation_data,

        average_precision=average_precision

    )

# =========================
# DETAIL PAGE
# =========================

@app.route("/detail/<int:id>")
def detail(id):

    laptop = df[df["id"] == id].iloc[0]

    product = {

        "id": laptop["id"],

        "nama": laptop["nama_laptop"],

        "harga": f"Rp {laptop['harga']:,}".replace(",", "."),

        "deskripsi": laptop["deskripsi"]

    }

    return render_template(
        "detail.html",
        product=product
    )

# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)