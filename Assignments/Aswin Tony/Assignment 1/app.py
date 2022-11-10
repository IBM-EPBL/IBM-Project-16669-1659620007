from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def form():
    return render_template("form.html")

@app.route("/display", methods = ["POST"])
def display_details():
    if request.method == "POST":
        name = request.form["nm"]
        phno = request.form["phno"]
        eml = request.form["eml"]
        return render_template("display.html", name=name, phno=phno, email=eml)

if __name__ == "__main__":
    app.run(debug=True)