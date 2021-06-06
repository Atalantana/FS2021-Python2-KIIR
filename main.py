from flask import request
from flask import Flask
from flask import render_template
from flask import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from collections import Counter
import easygui
import plotly.express as px
from plotly.offline import plot
import tkinter as tk
from jinja2 import Environment
import pandas as pd
import csv
from IPython.display import display


app = Flask("Peabuddy")


@app.route("/")
def home():
    kaktus = 30
    orchidee = 7
    zimmerpflanze = 3
    kraeuter = 3
    rose = 7
    palme = 30
    with open("data_plants.json", "r+") as outfile:
        pflanzen = json.load(outfile)
    check = datetime.now()
    return render_template("index.html", anzeige=pflanzen)


@app.route("/meinePflanzen.html", methods=["GET", "POST"])
def formular():
    pflanzen = []
    data_plants = {}
    if request.method == "POST":
        pftyp = request.form["Pflanzentyp"]
        pfname = request.form["Pflanzenname"]
        kfdatum = request.form["Kaufdatum"]
        wsdatum = request.form["Wassergabe"]

        data_plants["Pflanzentyp"] = pftyp
        data_plants["Pflanzenname"] = pfname
        data_plants["Kaufdatum"] = kfdatum
        data_plants["Wassergabe"] = wsdatum
        with open("data_plants.json", "r+") as outfile:
            pflanzen = json.load(outfile)
            pflanzen.append(data_plants)
            now = datetime.now()
            timestamp = datetime.timestamp(now)
            data_plants["Timestamp"]= str(timestamp)
        with open("data_plants.json", "w") as outfile:
            json.dump(pflanzen, outfile, indent=4)
        return render_template("meinePflanzen.html", anzeige=data_plants)
    else:
        return render_template("meinePflanzen.html", anzeige=False)


@app.route("/AllePflanzen", methods=["GET", "POST"])
def anzeigeAlle():
    with open("data_plants.json", "r+") as outfile:
        pflanzen = json.load(outfile)
        pflanzen_sorted = sorted(pflanzen, key=lambda k: k['Wassergabe'])


    return render_template("AllePflanzen.html", anzeige=pflanzen_sorted)
    return render_template("AllePflanzen.html", anzeige=False)


@app.route("/loesch", methods=["GET", "POST"])
def loesch():
    with open("data_plants.json", "r+") as outfile:
        pflanzen = json.load(outfile)
    if request.method == 'POST':
        timest = request.form["delpfl"]
        for eintr in pflanzen:
            timest_json = eintr["Timestamp"]
            print("JSON", timest_json)
            print("Form", timest)
            if timest == timest_json:
                pflanzen.remove(eintr)
            with open("data_plants.json", "w") as outfile:
                json.dump(pflanzen, outfile, indent=4)
        return redirect(url_for("anzeigeAlle"))
    return redirect(url_for("anzeigeAlle"))


@app.route("/Statistiken", methods=["GET", "POST"])
def statistiken():
    df = pd.read_json('data_plants.json')
    c = Counter(df["Pflanzentyp"])
    liste = c.most_common()
    p_type = [x[0] for x in liste]
    p_size = [x[1] for x in liste]
    fig = px.pie(names=p_type, values=p_size, title="Anzahl Pflanzentypen")
    viz_pie = plot(fig, output_type="div")
    return render_template("Statistiken.html", anzeige=viz_pie)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
