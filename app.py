from flask import Flask, render_template, request
from models.search import search_laptop
from laptop_parser import parse_laptop_specs
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

            "deskripsi": row["deskripsi"],

            "image": row["image"],

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

        {"query": "laptop gaming",        "precision": 0.8},
        {"query": "laptop mahasiswa",     "precision": 0.7},
        {"query": "laptop editing",       "precision": 0.9},
        {"query": "laptop murah",         "precision": 0.6},
        {"query": "laptop RTX",           "precision": 0.9},
        {"query": "laptop office",        "precision": 0.8},
        {"query": "laptop desain grafis", "precision": 0.8},
        {"query": "laptop tipis",         "precision": 0.7},
        {"query": "laptop coding",        "precision": 0.8},
        {"query": "laptop SSD",           "precision": 0.9},

    ]

    # =========================
    # AVERAGE PRECISION
    # =========================

    average_precision = round(
        sum(item["precision"] for item in evaluation_data) / len(evaluation_data),
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

    nama      = laptop["nama_laptop"]
    deskripsi = laptop["deskripsi"]

    # =========================
    # RANK & SCORE
    # =========================

    rank  = request.args.get("rank", type=int)
    score = request.args.get("score", type=float)

    # =========================
    # PARSE SPECS
    # =========================

    specs = parse_laptop_specs(nama, deskripsi)

    # =========================
    # PRODUCT DATA
    # =========================

    product = {

        "id": laptop["id"],

        "nama": nama,

        "harga": f"Rp {laptop['harga']:,}".replace(",", "."),

        "deskripsi": deskripsi,

        "image": laptop["image"],

        # =========================
        # SPECS
        # =========================

        "processor": specs["processor"],
        "gpu": specs["gpu"],
        "ram": specs["ram"],
        "display": specs["display"],
        "storage": specs["storage"],
        "tags": specs["tags"],
        "tagline": specs["tagline"],
        "deskripsi_panjang": specs["deskripsi_panjang"],
        "keunggulan": specs["keunggulan"],

        # =========================
        # SIMILARITY
        # =========================

        "rank": rank,
        "score": score,

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