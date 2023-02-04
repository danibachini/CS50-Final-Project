# read https://www.loekvandenouweland.com/content/full-path-in-zsh-shell.html

# How to use bcrypt: 
# https://blog.carsonevans.ca/2020/08/02/storing-passwords-in-flask/ 
# https://www.npmjs.com/package/bcrypt?activeTab=readme

import sys
import os
import mysql.connector
from bcrypt import hashpw, checkpw, gensalt
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from datetime import datetime
import re
from galeeza.helpers import apology

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Thg489!asf",
    database="galeeza"
)


@app.route("/")
# @login_required
def index():
    """Your Trips - Display all the planned trips and old trips"""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        return "TODO"
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

    else:
        return render_template("login.html")




@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Register user"""
    
    if request.method == "POST":
        
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        confirmation = request.form["confirmation"]

        mycursor = db.cursor()

        select_query = f"SELECT * FROM users WHERE email='{email}'"
        mycursor.execute(select_query)
        result = mycursor.fetchone()

        if result:
            return apology("There's already an account registered with this email")
        if first_name == "" or last_name == "" or email == "" or password == "" or confirmation == "":
            return apology("All fields are required")
        if password != confirmation:
            return apology("Password and Confirmation don't match")
        if len(password) < 8:
            return apology("Password must have at least 8 characters")
        if not re.search("[a-z]", password):
            return apology("Password must contain at least 1 lowercase letter")
        if not re.search("[A-Z]", password):
            return apology("Password must contain at least 1 uppercase letter")
        else: 
            hash = password
            insert_query = f"INSERT INTO users (first_name, last_name, email, hash) VALUES('{first_name}', '{last_name}', '{email}', '{hash}')"
            mycursor.execute(insert_query)
            db.commit()
            return redirect("/")

    else:
        return render_template("signup.html")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")




@app.route("/plan")
def plan():
    """Take the user to plan the trip"""
    return render_template("plan.html")


@app.route("/profile")
def profile():
    """Display the user's profile"""
    return render_template("profile.html")
