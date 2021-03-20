from flask import Flask
from flask import render_template


app = Flask("Homebuddy")

@app.route("/")
def index():
    return render_template("index.html", name="Irene")


@app.route("/test")
def test_seite():
    return"funktioniert"

if __name__ == "__main__":
    app.run(debug=True, port=5000)