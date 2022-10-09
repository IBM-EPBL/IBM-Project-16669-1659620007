from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scorecalc")
def score_calc():
    return render_template("scorecalc.html")

@app.route("/finalscore", methods=["GET"])
def final_score():
    if request.method == "GET":
        res = request.args.getlist("mks")
        app.logger.info(res)
        total = 0
        for i in range(len(res)):
            total += int(res[i])
        return render_template('total.html', total=total)

@app.route("/feedback")
def feedback():
    return render_template('feedback.html')

if __name__ == "__main__":
    app.run(debug=True)