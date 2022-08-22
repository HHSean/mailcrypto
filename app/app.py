from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect,
    Response,
    make_response,
    send_file,
)
import os
import random
import util

################################################################################
CONTRACT = "0x616d197a29e50ebd08a4287b26e47041286f171d"
################################################################################


app = Flask(__name__, static_folder="src/", template_folder="src/html/")
app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
)


# before request redirect to https
@app.before_request
def before_request():
    if request.url.startswith("http://") and not "127.0." in request.url:
        return redirect(request.url.replace("http://", "https://", 301))


# sanity check route
@app.route("/ping", methods=["GET"])
def ping_pong():
    return render_template("pong.html")


# home
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

# send
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "GET":
        return render_template("send.html")
    elif request.method == "POST":
        email = request.form["email"]
        amount = request.form["amount"]

        # send email
        util.send_email(email, amount=amount)
        return render_template("confirmation.html")


@app.route("/claim/<key>", methods=["GET"])
def claim(key):
    return render_template("claim.html", key=key)


@app.route("/unsubscribe/<key>", methods=["GET"])
def unsubscribe(key):
    return render_template("unsubscribe.html", key=key)   


@app.route("/confirmation", methods=["GET"])
def confirmation():
    return render_template("confirmation.html")
    

if __name__ == "__main__":    
    # differentiate between local and production
    if "ENV" in os.environ:
        if os.environ["ENV"] == "PROD":
            app.run(debug=False)
        elif os.environ["ENV"] == "DEV":
            app.run(debug=True)
    else:
        app.run(debug=True)
