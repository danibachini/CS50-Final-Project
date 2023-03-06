# read https://www.loekvandenouweland.com/content/full-path-in-zsh-shell.html

# How to use bcrypt: 
# https://blog.carsonevans.ca/2020/08/02/storing-passwords-in-flask/ 
# https://www.npmjs.com/package/bcrypt?activeTab=readme

# import sys
# import os
# import json
import mysql.connector  # documentation: https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html 
from bcrypt import hashpw, checkpw, gensalt
from flask import Flask, redirect, render_template, request, session, flash, jsonify
from flask_session import Session
# import pymysql
# from datetime import datetime
import re
from galeeza.helpers import apology, login_required

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

datab = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Thg489!asf",
    database="galeeza"
)

mycursor = datab.cursor()

# CHECK DB DESIGN AT https://app.sqldbm.com/MySQL/Edit/p249319/ 

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

        # check on the table if there's a row where email equals the email provided by the user
        select_query = ("SELECT * FROM users WHERE email=%s")
        user_email = (email,)
        mycursor.execute(select_query, user_email)
        result = mycursor.fetchone()

        if result:
            return apology("There's already an account registered with this email")
        
        # check some constraints about the inputs
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

        # if everything about the inputs is good, insert the user to the table
        else: 
            # hash password with salt
            hash = hashpw(password.encode('utf-8'), gensalt())

            # store the user into the table
            insert_query = ("INSERT INTO users (first_name, last_name, email, hash) VALUES(%s, %s, %s, %s)")
            data_user = (first_name, last_name, email, hash)
            mycursor.execute(insert_query, data_user)
            datab.commit()

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

        # check on the datab table the row where email equals the email provided by the user
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



@app.route("/logout", methods=["GET", "POST"])
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/preferences", methods=["GET", "POST"])
@login_required
def preferences():
    """Take the user to fill in their preferences"""

    if request.method == "POST":
        selected_options = request.get_json()
        print(selected_options)

        # check the id of the user preferences in the user_preferences table
        id_query = ("SELECT id FROM user_preferences WHERE id_user=%s")
        session_user = (session["user_id"],)
        mycursor.execute(id_query, session_user)
        id_pref, = mycursor.fetchone()  # the comma is to use tuple unpacking to extract the value 

        for i in selected_options: 
            # check on the datab table the row where category equals the category selected by the user
            select_query = ("SELECT category FROM types WHERE category=%s")
            category = (i,)
            mycursor.execute(select_query, category)
            result = mycursor.fetchone()

            # add all the preferences the user selected to the table chosen_preferences
            if result:
                # get the id of the selected category in the types table
                types_query = ("SELECT id FROM types WHERE category=%s")
                category_type = (i,)
                mycursor.execute(types_query, category_type)
                category_id, = mycursor.fetchone()  # the comma is to use tuple unpacking to extract the value 

                # get the id of the category 
                find_query = ("SELECT id_user_pref FROM chosen_preferences WHERE id_type=%s")
                find_type = (category_id,)
                mycursor.execute(find_query, find_type)
                find_result = mycursor.fetchone()

                # if the category does not exist in the user's chosen_preferences table, add it
                if not(find_result): 
                    # add the user selected preference to the chosen_preferences table
                    insert_pref = ("INSERT INTO chosen_preferences (id_type, id_user_pref, bool_value) VALUES (%s, %s, %s)")
                    values_pref = (category_id, id_pref, 1)
                    mycursor.execute(insert_pref, values_pref)
                    datab.commit()

            # add daily cost in the table user_preferences
            else:
                check_query = ("SELECT id_user FROM user_preferences WHERE id_user=%s")
                id_user = (session["user_id"],)
                mycursor.execute(check_query, id_user)
                result_id = mycursor.fetchone()

                # if user had previously selected a value, update it for the new value
                if result_id:
                    update_query = ("UPDATE user_preferences SET cost_day=%s WHERE id_user=%s")
                    new_cost = (i,session["user_id"])
                    mycursor.execute(update_query, new_cost)
                    datab.commit()

                # if first time user is selecting a value, add it to the table
                else:
                    insert_query = ("INSERT INTO user_preferences (cost_day, id_user) VALUES (%s, %s)")
                    values_user = (i, session["user_id"])
                    mycursor.execute(insert_query, values_user)
                    datab.commit()

        return redirect("plan.html")

    else:
        return render_template("preferences.html")



@app.route("/plan", methods=["GET", "POST"])
@login_required
def plan():
    """Take the user to plan the trip"""

    if request.method == "POST":
        return "TODO"

    else:
        # PSEUDOCODE
        # user clicks on plan
        # check on the datab if the preferences with that id exist (aka row = 1)
        # if it doesn't exist - redirect user to form
        # if it does exist - redirect user to plan




        # check on the datab table if there is at least one row with the session user_id of the user logged in
        select_query = ("SELECT * FROM user_preferences WHERE id_user=%s") # <<<<---!!!!! CHANGE THIS it doesn't guarantee the user answered all the questions !!!!
        id_user = (session["user_id"],)
        mycursor.execute(select_query, id_user)
        result = mycursor.fetchone()

        # if there's no row with the session user_id logged in
        if not result:
            return redirect("/preferences")

        # if the user already filled in their preferences
        return render_template("plan.html")






@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Display the user's profile"""
    return render_template("profile.html")
