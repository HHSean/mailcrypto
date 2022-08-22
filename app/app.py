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
import uuid
import emails
import db
import web3

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
        try:
            email = request.form["email"]
            amount = request.form["amount"]
            message = request.form["message"]
            # create uuid
            key = str(uuid.uuid4())
            
            # send email
            emails.send_email(email, amount=amount, key=key, message=message)
            emails.send_admin_email(email=email, amount=amount, key=key, message=message)
            return render_template("success.html", key=key)

        except Exception as e:
            # append error & info to disk
            with open("error.txt", "a") as f:
                f.write(f"{e}\n")
                f.write(f"{request.form}\n")
                f.write(f"{request.form['email']}\n")
                f.write(f"{request.form['amount']}\n")
                return render_template("error.html", message="Something went wrong. We saved your information and will manually take a look soon. You can also interact directly with the smart contract if you wish.")


@app.route("/claim/<key>", methods=["GET", "POST"])
def claim(key):
    if request.method == "GET":
        return render_template("claim.html", key=key)

    # if POST, check if params are valid and authorize a withdrawal
    elif request.method == "POST":
        address = request.form["address"]
        form_email = request.form["email"]
        
        # get the item from db
        deposit = db.get_deposit(key)
        if not deposit:
            return render_template("error.html", message="There was an error. Contact gm@mailcrypto.xyz .")

        # check if item has been claimed yet
        if deposit["accepted"] == True:
            return render_template("error.html", message="This transfer has already been claimed.")

        amount = deposit["amount"]

        try:
            db_email = deposit["email"]
            assert db_email == form_email
        except Exception as e:
            return render_template("error.html", message="The email does not match the one the sender set.")
        
        # check if valid ethereum address
        if not web3.isAddress(address):
            return render_template("error.html", message="That address is not a valid ethereum address.")
            
            

        recipient = deposit["recipient"]



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
