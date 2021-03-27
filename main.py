from flask import Flask
from flask import render_template

app = Flask("Peabuddy")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/meinePflanzen")
def meinePflanzen():
    return render_template("meinePflanzen.html")

@app.route("/Materialverwaltung")
def materialverwlatung():
    return render_template("Materialverwaltung.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
