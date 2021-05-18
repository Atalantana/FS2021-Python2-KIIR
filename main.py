from flask import request
from flask import Flask
from flask import render_template
from flask import json
import pandas as pd
import csv


app = Flask("Peabuddy")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/meinePflanzen")
def meinePflanzen():
    return render_template("meinePflanzen.html")


@app.route("/result", methods=["GET", "POST"])
def result():
    data_plants = {}
    if request.method == "POST":
        pftyp = request.form["pflanzenauswahl"]
        pfname = request.form["Pflanzenname"]
        kfdatum = request.form["Kaufdatum"]
        wsdatum = request.form["Wassergabe"]
        data_plants["Pflanzen"] = []
        data_plants["Pflanzen"].append({
                "Pflanzentyp": pftyp,
                "Pflanzenname": pfname,
                "Kaufdatum": kfdatum,
                "Letzte Wassergabe":wsdatum
        })
        with open("data_plants.json", "w") as outfile:
                json.dump(data_plants, outfile)
        with open("data_plants.json", "r") as outfile:
            anzeige = json.load(outfile)
            anzeige1 = [value for key, value in anzeige.items()][0]
    return render_template("meinePflanzen.html", anzeige=anzeige1)



@app.route("/Materialverwaltung", methods=["GET", "POST"])
def materialverwaltung():
    return render_template("Materialverwaltung.html")



if __name__ == "__main__":
    app.run(debug=True, port=5000)
