from flask import request
from flask import Flask
from flask import render_template
from flask import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import easygui
import plotly.express as px
import tkinter as tk
from jinja2 import Environment
import pandas as pd
import csv


app = Flask("Peabuddy")


@app.route("/")
def home():
    return render_template("index.html")


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
    return render_template("AllePflanzen.html", anzeige=pflanzen)
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
    return render_template("Statistiken.html")




if __name__ == "__main__":
    app.run(debug=True, port=5000)
