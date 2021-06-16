from flask import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from collections import Counter
import plotly.express as px
from plotly.offline import plot
import pandas as pd


app = Flask("Peabuddy")


# =========================================================================
#            Startseite / Landing Page
# =========================================================================


@app.route("/")
def home():
    """
    Startseite mit gleichzeitiger Berechnung der Anzahl vergangener Tage seit letzter Wassergabe sowie der Anzeige aller
     Pflanzen mit den Attributen Pflanzentyp und Pflanzenname,
    Die Tage werden in keiner Datei gespeichert.
    Die Daten werden mithilfe der lambda Funktion sortiert. Das älteste Datum wird immer zuoberst angezeigt
    Für die korrekte Berechnung der vergangenen Tage wird mithilfe datetime.strptime(item["Wassergabe"], "%Y-%m-%d")
    das Datum aus der json-Datei (["Wassergabe"]) in ein
    rechenbares Datum (Datenwerte) umgewandelt, da das Datum in der JSON-Datei "data_plants.json" als String
    abgespeichert ist.

    """
    with open("data_plants.json", "r+") as outfile:
        pflanzen = json.load(outfile)
        pflanzen_sorted = sorted(pflanzen, key=lambda k: k['Wassergabe'])
        for item in pflanzen:
            minus = datetime.strptime(item["Wassergabe"], "%Y-%m-%d")
            today = datetime.today()
            toddate = today.date()
            mindate = minus.date()
            diffdays = toddate - mindate
            item["Tage"] = str(diffdays.days)
    return render_template("index.html", anzeige=pflanzen_sorted)


# =========================================================================
#            Meine Pflanzen / Eingabeformular
# =========================================================================


@app.route("/meinePflanzen.html", methods=["GET", "POST"])
def formular():
    """
    In der Funktion formular() werden die im Formular eingegebenen Daten in Form eines Dictionaries einer JSON-Datei
    "data_plants.json" übergeben und in einer Liste abgespeichert
    Mit dem Betätigen des Buttons "Absenden" auf der Seite "Eintrag anlegen" wir der Befehl in Auftrag gegeben,
    eine JSON-Datei zu öffnen und dabei die eingegebenen Formulardaten
    "abzuholen", sie in einer Variablen zu speichern. Die Variablen bzw. deren Werte werden einem Key zugeordnet,
    welcher sich im Dictionary data_plants befindet. Das so entstandene Dictionary
     wird nun in einer Liste in der JSON-Datei "data_plants.json" abgelegt. Zusätzlich erhält der Eintrag
     zudem noch eine Timestamp, welche mit in der JSON-Datei gespeichert wird und für die Bearbeitung bzw.
     das Löschen und Aktualisieren der Listeneinträge genutzt wird.

    """
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


# =============================================================================
#           Alle Pflanzen / Anzeige aller Listeneinträge in der JSON-Datei
# =============================================================================


@app.route("/AllePflanzen", methods=["GET", "POST"])
def anzeigeAlle():
    """
    Diese Funktion lässt die Listeneinträge - geordnet nach ältester Wassergabe - der JSON-Datei "data_plants.json" auf
    der Übersichtsseite "Alle Pflanzen" darstellen. Zusätzlich wird mithilfe "datetime" die
    vergangenen Tage seit dem Datum der letzten Wassergabe berechnet. In der Variable "minus" wird das für die
    Berechnung notwendige Datum aus der JSON-Datei
    "geholt" und von einem String in ein "echtes" Datumsformat umgewandelt und gespeichert,
    damit man die Berechnung durchführen kann.

    Die Differenz zwischen Wassergabedatum und aktuellem Datum wird als value dem Key "Tage" zugeordnet,
    welcher wiederum zum Dictionary pflanzen gehört. Er wird jedoch
    nicht in der JSON-Datei "data_plants.json" abgespeichert sondern lediglich für die Anzeige mit Jinja
    auf der HTML-Seite "Alle Pflanzen" verwendet.
    """
    with open("data_plants.json", "r+") as outfile:
        pflanzen = json.load(outfile)
        pflanzen_sorted = sorted(pflanzen, key=lambda k: k['Wassergabe'])
        for item in pflanzen:
            minus = datetime.strptime(item["Wassergabe"], "%Y-%m-%d")
            today = datetime.today()
            toddate = today.date()
            mindate = minus.date()
            diffdays = toddate - mindate
            item["Tage"] = str(diffdays.days)
        return render_template("AllePflanzen.html", anzeige=pflanzen_sorted)
    return render_template("AllePflanzen.html", anzeige=False)


# =================================================================================
#          Alle Pflanzen / Löschen einzelner Listeneinträge in der JSON-Datei
# =================================================================================


@app.route("/loesch", methods=["GET", "POST"])
def loesch():
    """
    Mit dem Klick auf den Button "Löschen" öffnet sich ein neuer Pfad "loesch", es wird die Timestamp
    des entsprechenden Listeneintrages angefordert und mit den Timestamps in der JSON-Datei "data_plants.json"
    verglichen und - falls die Timestamps übereinstimmen - wird der entsprechende Listeneintrag gelöscht und man wird
    mittels redirect wieder zurück zur originalen "Alle Pflanzen"-Seite weitergeleitet.

    """
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


# =====================================================================================
#          Alle Pflanzen / Aktualisieren einzelner Listeneinträge in der JSON-Datei
# =====================================================================================


@app.route("/aktual", methods=["GET", "POST"])
def aktual():
    """
    Analog zur Funktion "Löschen" eines einzelnen Listeneintrags wird hier in dieser Funktion das Wassergabedatum
    aktualisiert Mit dem gleichen Vorgehen in der Funktion "loesch" anstelle
    dem Löschen des gesamten Listeneintrags wird einfach ein einzelner Wert der Liste ("Wassergabe")
    mit einem neuen Wert (aktuelles Datum) ersetzt / überschrieben.

    Auch hier wird man mit Klick auf den Button wieder auf einen neuen Pfad "geleitet" und mit "redirect" wird man wieder
     zurück auf die Seite "Alle Pflanzen" verwiesen.
    """
    with open("data_plants.json", "r+") as outfile:
        pflanzen = json.load(outfile)
    if request.method == 'POST':
        uptime = request.form["aktual"]
        for eintr in pflanzen:
            upjson = eintr["Timestamp"]
            if uptime == upjson:
                eintr["Wassergabe"] = datetime.today().strftime('%Y-%m-%d')
            with open("data_plants.json", "w") as outfile:
                json.dump(pflanzen, outfile, indent=4)
        return redirect(url_for("anzeigeAlle"))
    return redirect(url_for("anzeigeAlle"))


# =====================================================================================
#         Statistiken / Anzeige Pie-Chart
# =====================================================================================


@app.route("/Statistiken", methods=["GET", "POST"])
def statistiken():
    """
    Mithilfe eines Counters werden die Pflanzentypen in der JSON-Datei gezählt. In der Variable "liste" wird eine Liste
     mit Tupeln abgespeichert. Jedes Tupel enthält einen Pflanzentyp
    sowie die Anzahl gezählter Pflanzentypen. Nun werden mit einer for-Schleife
    die jeweiligen ersten und zweiten Elemente der Tupel je in einer Liste gespeichert. Die so neu gefüllten
    Listen mit den Tupelwerten werden der Funktion für die Erstellung einer Pie-Chart übergeben.

    """
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
