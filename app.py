import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

from helpers import apology, login_required


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"

    response.headers["Expires"] = 0

    response.headers["Pragma"] = "no-cache"

    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()

app.config["SESSION_PERMANENT"] = False

app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///hydrateU.db")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):

            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):

            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",

                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):

            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        date = datetime.today().strftime('%Y-%m-%d')

        loggedBefore = len(db.execute("SELECT * FROM dailyGoals WHERE user_id = :user_id AND date = :date", user_id=session["user_id"], date=date))

        if loggedBefore == 0:

            db.execute("INSERT INTO dailyGoals (user_id, date) VALUES (:user_id, :date)", user_id=session["user_id"], date=date)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":

        return render_template("register.html")
    else:
        username = request.form.get("username")

        password = request.form.get("password")

        confirmation = request.form.get("confirmation")

        firstName = request.form.get("firstName")

        lastName = request.form.get("lastName")

        #check conditions
        if not username:

            return apology("Enter a username.")

        elif not password:

            return apology("Enter a password.")

        elif len(password) < 3:

            return apology("Password too short.")

        elif confirmation != password:

            return apology("Passwords do not match.")

        elif not firstName:

            return apology("Enter a first name.")

        elif not lastName:

            return apology("Enter a last name.")

        #generate password hash
        passHash = generate_password_hash(password)

        users = db.execute("SELECT * FROM users")

        #check if username is taken
        for user in users:

            if username == user["username"]:

                return apology("That username is taken.")

        #insert new row in table
        db.execute("INSERT INTO users (username, hash, first_name, last_name) VALUES (:username, :passHash, :firstName, :lastName)", username=username, passHash=passHash, firstName=firstName, lastName=lastName)

        return redirect("/login")

@app.route("/goals", methods=["GET", "POST"])
@login_required
def goals():
    if request.method == "GET":
        date = datetime.today().strftime('%Y-%m-%d')

        goal = db.execute("SELECT goal FROM dailyGoals WHERE user_id = :user_id AND date = :date", user_id=session["user_id"], date=date)

        #get user's current goal
        currentGoal = goal[0]["goal"]

        return render_template("goals.html", goal=currentGoal)
    else:
        updateGoal = request.form.get("updateGoal")

        #get current date

        date = datetime.today().strftime('%Y-%m-%d')

        db.execute("UPDATE dailyGoals SET goal = :updateGoal WHERE user_id = :user_id AND date = :date", updateGoal=updateGoal, user_id=session["user_id"], date=date)

        return redirect("/")

@app.route("/")
def index():
    '''Starter page'''
    glasses = db.execute("SELECT SUM(glassesDrank) FROM dailyGoals")

    #get sum of all glasses drank

    glassesDrank = glasses[0]["SUM(glassesDrank)"]

    users = db.execute("SELECT COUNT(username) FROM users")

    #get count of all users

    usersHad = users[0]["COUNT(username)"]

    goals = db.execute("SELECT AVG(goal) FROM dailyGoals")

    goals1 = goals[0]["AVG(goal)"]

    #get average goal set by users

    avgGoal = round(goals1, 2)

    return render_template("index.html", glassesDrank=glassesDrank, usersHad=usersHad, avgGoal=avgGoal)

@app.route("/hydrationLog", methods=["GET", "POST"])
@login_required
def hydrationLog():
    if request.method == "GET":

        date = datetime.today().strftime('%Y-%m-%d')

        #selectDict = db.execute("SELECT * FROM dailyGoals WHERE user_id = :user_id AND date = :date", user_id=session["user_id"], date=date)

        #dict of daily logs of all users

        selectDict = db.execute("SELECT * FROM dailyGoals WHERE user_id = :user_id", user_id=session["user_id"])

        goal = db.execute("SELECT goal FROM dailyGoals WHERE user_id = :user_id AND date = :date", user_id=session["user_id"], date=date)

        currentGoal = goal[0]["goal"]

        print(selectDict)

        glassDrank = db.execute("SELECT glassesDrank FROM dailyGoals WHERE user_id = :user_id AND date = :date", user_id=session["user_id"], date=date)

        glassesDrank = int(glassDrank[0]["glassesDrank"])

        currentGlassesDrank = glassesDrank

        if currentGlassesDrank >= currentGoal: #check if user's reached their goal
            db.execute("UPDATE dailyGoals SET reachedGoal = :true WHERE user_id = :user_id AND date = :date", user_id=session["user_id"], true = True, date=date)
        elif currentGlassesDrank < currentGoal:
            db.execute("UPDATE dailyGoals SET reachedGoal = :false WHERE user_id = :user_id AND date = :date", user_id=session["user_id"], false = False, date=date)

        reached = 0
        notReached = 0

        for day in selectDict:
            if day["reachedGoal"] == 1:
                reached += 1
            else:
                notReached += 1

        successRate = round(((reached)/(reached + notReached) * 100), 2)

        return render_template("hydrationLog.html", goal=currentGoal, everyDayData=selectDict, currentGlassesDrank=currentGlassesDrank, reached=reached, notReached=notReached, successRate=successRate)
    else:

        date = datetime.today().strftime('%Y-%m-%d')

        updateGlasses = int(request.form.get("addGlass"))

        glassDrank = db.execute("SELECT glassesDrank FROM dailyGoals WHERE user_id = :user_id AND date = :date", user_id=session["user_id"], date=date)

        glassesDrank = int(glassDrank[0]["glassesDrank"])

        goal = db.execute("SELECT goal FROM dailyGoals WHERE user_id = :user_id AND date = :date", user_id=session["user_id"], date=date)

        currentGoal = goal[0]["goal"]

        print(currentGoal)

        currentGlassesDrank = updateGlasses + glassesDrank

        if currentGlassesDrank >= currentGoal: #update if goal was reached
            db.execute("UPDATE dailyGoals SET reachedGoal = :true WHERE user_id = :user_id AND date = :date", user_id=session["user_id"], true = True, date=date)
        elif currentGlassesDrank < currentGoal:
            db.execute("UPDATE dailyGoals SET reachedGoal = :false WHERE user_id = :user_id AND date = :date", user_id=session["user_id"], false = False, date=date)

        db.execute("UPDATE dailyGoals SET glassesDrank = :glassesDrank WHERE user_id = :user_id AND date = :date", glassesDrank=currentGlassesDrank, user_id=session["user_id"], date=date)

        return redirect("/hydrationLog")


@app.route("/crisis")
@login_required
def crisis():

    return render_template("crisis.html")

@app.route("/contribute")
@login_required
def contribute():

    return render_template("contribute.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):

        e = InternalServerError()

    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:

    app.errorhandler(code)(errorhandler)
