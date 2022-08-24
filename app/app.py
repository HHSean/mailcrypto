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
import dotenv
import crypto
dotenv.load_dotenv("../.env")


################################################################################
CONTRACT = os.getenv("CONTRACT_ADDRESS")
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
    return render_template("home.html", contractAddress=CONTRACT)

# send
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "GET":
        return render_template("send.html", contractAddress=CONTRACT)
    elif request.method == "POST":
        tx_hash = "0x"
        try:
            email = request.form["email"]
            amount = request.form["amount"]
            message = request.form["message"]
            tx_hash = request.form["txHash"]
            sender = request.form["senderAddress"]
            deposit_index = request.form["depositIndex"]

            print(f"email: {email}, amount: {amount}, message: {message}, tx_hash: {tx_hash}, deposit_index: {deposit_index}")

            # create uuid
            key = str(uuid.uuid4())
            # make deposit in db
            db.insert_deposit(sender, email, key, amount, message, tx_hash, deposit_index)
            
            # send email
            emails.send_email(email, amount=amount, key=key, message=message)
            emails.send_admin_email(email=email, amount=amount, key=key, message=message)
            return render_template("success.html", tx_hash=tx_hash, message='Your transaction has been sent!')

        except Exception as e:
            print(e)
            # append error & info to disk
            with open("error.txt", "a") as f:
                f.write(f"{e}\n")
                f.write(f"{request.form}\n")
                f.write(f"{request.form['email']}\n")
                f.write(f"{request.form['amount']}\n")
                return render_template("error.html", message="There was an error on our end. We saved your information and will manually take a look soon. You can also take a look at the smart contract anytime and retrieve your funds.", tx_hash=tx_hash)


@app.route("/claim/<key>", methods=["GET", "POST"])
def claim(key):
    if request.method == "GET":
        try:
            # check if key in db
            if not db.check_key(key):
                return render_template("error.html", message="Please check your email address for the correct claiming link.")

            # get deposit
            deposit = db.get_deposit(key)
            return render_template("claim.html", deposit=deposit, key=key)
        except Exception as e:
            # reload page
            return redirect(f"/claim/{key}")

    # if POST, check if params are valid and authorize a withdrawal
    elif request.method == "POST":
        to_address = request.form["to_address"]
        print(f"to_address: {to_address}, key: {key}")
        
        if not db.check_key(key):
            return render_template("error.html", message="There was an error. Contact gm@mailcrypto.xyz .")

        # get the item from db
        deposit = db.get_deposit(key)

        # check if item has been claimed yet
        if deposit["accepted"] == True:
            return render_template("error.html", message="This transfer has already been claimed.")

        ## nice idea but useless ##
        # try:
        #     db_email = deposit["email"]
        #     assert db_email == form_email
        # except Exception as e:
        #     return render_template("error.html", message="The email does not match the one the sender set.")
        
        # check if valid ethereum address
        if not crypto.check_if_address_is_valid(to_address):
            return render_template("error.html", message="That address is not a valid ethereum address.")

        

        # call smart contract 
        index  = deposit["deposit_index"]
        tx_receipt, tx_hash = crypto.make_withdrawal(index, to_address)

        # update db
        db.update_deposit(key, True)


        return render_template("success.html", message="Your funds have been claimed! They are now in your wallet.", tx_hash=tx_hash)


@app.route("/claim", methods=["GET"])
def claim_base():
    return render_template("claim_base.html")



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
