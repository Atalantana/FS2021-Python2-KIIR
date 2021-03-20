from flask import Flask, request
from flask import render_template

app = Flask("Peabuddy")

@app.route("/")
def home():
    return render_template("land_page.html")




if __name__ == "__main__":
    app.run(debug=True, port=5000)

#@app.route("/", methods=["GET", "POST"])
#def index():
    #if request.method == 'POST':
        #ziel_person = request.form['vorname']
        #rueckgabe_string = "Hello " + ziel_person + "!"
        #return rueckgabe_string

    #return render_template("land_page.html")


