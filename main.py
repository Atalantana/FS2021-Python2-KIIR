from flask import request
from flask import Flask
from flask import render_template

app = Flask("Peabuddy")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/meinePflanzen")
def meinePflanzen():
    return render_template("meinePflanzen.html")


@app.route("/meinePflanzen", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        pftyp = request.form["pflanzenauswahl"]
        pfname = request.form["Pflanzenname"]
        kfdatum = request.form["Kaufdatum"]
        wsdatum = request.form["Wassergabe"]
        result= pftyp+" "+pfname+" "+kfdatum+" "+wsdatum
    return render_template("/result.html", result=result )




@app.route("/Materialverwaltung")
def materialverwlatung():
    return render_template("Materialverwaltung.html")




if __name__ == "__main__":
    app.run(debug=True, port=5000)
