# read https://www.loekvandenouweland.com/content/full-path-in-zsh-shell.html

# How to use bcrypt: 
# https://blog.carsonevans.ca/2020/08/02/storing-passwords-in-flask/ 
# https://www.npmjs.com/package/bcrypt?activeTab=readme

import sys
import os
import mysql.connector  # documentation: https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html 
from bcrypt import hashpw, checkpw, gensalt
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
# import pymysql
from datetime import datetime
import re
from galeeza.helpers import apology, login_required

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

mycursor = db.cursor()

@app.route("/")
@login_required
def index():
    """Your Trips - Display all the planned trips and old trips"""
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Register user"""
    
    if request.method == "POST":
        
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        confirmation = request.form["confirmation"]

        # check on the db table the row where email equals the email provided by the user
        select_query = ("SELECT * FROM users WHERE email=%s")
        user_email = (email,)
        mycursor.execute(select_query, user_email)
        result = mycursor.fetchone()

        # check some constraints about the input
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

        # if everything about the input is good, insert the user to the table
        else: 
            # hash password with salt
            hash = hashpw(password.encode('utf-8'), gensalt())

            # store the user into the table
            insert_query = ("INSERT INTO users (first_name, last_name, email, hash) VALUES(%s, %s, %s, %s)")
            data_user = (first_name, last_name, email, hash)
            mycursor.execute(insert_query, data_user)
            db.commit()

            # get the user id from the table users
            select_query = ("SELECT * FROM users WHERE email=%s")
            user_email = (email,)
            mycursor.execute(select_query, user_email)
            result = mycursor.fetchone()

            # store the user id in the session
            session["user_id"] = result[0]
            return redirect("/")

    else:
        return render_template("signup.html")

    # ------- FIX BROKEN IMAGE SIGN UP ------------ 


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        
        email = request.form["email"]
        password = request.form["password"]

        # check if email or password were blank
        if email == "" or password == "":
            return apology("All fields are required")

        # check on the db table the row where email equals the email provided by the user
        select_query = ("SELECT * FROM users WHERE email=%s")
        user_email = (email,)
        mycursor.execute(select_query, user_email)
        result = mycursor.fetchone()

        # if there's no row with the mail provided
        if not result:
            return apology("There's no account registered with this email")
        
        # check if the password match with the result from the table
        check_user = ("SELECT hash FROM users WHERE email=%s")
        user_email = (email,)
        mycursor.execute(check_user, user_email)
        user = mycursor.fetchone()
        hash = user[0].encode('utf-8')

        # If password provided by the user doesn't match the hashed password in the table
        if not checkpw(password.encode('utf-8'), hash):
            return apology("Password is incorrect")
        
        # Remember which user has logged in
        session["user_id"] = result[0] 

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")




@app.route("/plan")
@login_required
def plan():
    """Take the user to plan the trip"""
    return render_template("plan.html")



@app.route("/profile")
@login_required
def profile():
    """Display the user's profile"""
    return render_template("profile.html")
