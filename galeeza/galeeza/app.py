
import mysql.connector  
from bcrypt import hashpw, checkpw, gensalt
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import datetime
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

mycursor = datab.cursor(buffered=True)


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
        mycursor.execute("SELECT * FROM users WHERE email=%s", (email,))
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
            mycursor.execute("INSERT INTO users (first_name, last_name, email, hash) VALUES(%s, %s, %s, %s)", (first_name, last_name, email, hash))
            datab.commit()

            # get the user id from the table users
            mycursor.execute("SELECT * FROM users WHERE email=%s", (email,))
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
        mycursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        result = mycursor.fetchone()

        # if there's no row with the mail provided
        if not result:
            return apology("There's no account registered with this email")
        
        # check if the password match with the result from the table
        mycursor.execute("SELECT hash FROM users WHERE email=%s", (email,))
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
        # print(selected_options)

        for i in selected_options: 
            
            if i.isnumeric(): # if it's numeric, then it's the user's cost
                # check on the user_preferences table if there's an id_user compatible with the id of the user
                mycursor.execute("SELECT id FROM user_preferences WHERE id_user=%s", (session["user_id"],))
                existing_id_user = mycursor.fetchone()
                
                if not existing_id_user: # if it doesn't exist a record of the user in this table, add it into it
                    mycursor.execute("INSERT INTO user_preferences (id_user, cost_day) VALUES (%s, %s)", (session["user_id"], i))
                    datab.commit()
                
                else: # if there is a record of the user in this table, update it 
                    mycursor.execute("UPDATE user_preferences SET cost_day=%s WHERE id_user=%s", (i, session["user_id"]))
                    datab.commit()
                
            else: # if it comes to else, it's a category
                # get the id of the category in the categories table
                mycursor.execute("SELECT id FROM categories WHERE category=%s", (i,))
                find_result = mycursor.fetchone()[0]

                # check on the chosen_categories table if there's an id_category compatible with the id of the category selected by the user
                mycursor.execute("SELECT id_category FROM chosen_categories WHERE id_category=%s AND id_user=%s", (find_result, session["user_id"]))
                category_id = mycursor.fetchone()

                if not category_id: 
                    # add the user selected preference to the chosen_categories table
                    mycursor.execute("INSERT INTO chosen_categories (id_category, id_user) VALUES (%s, %s)", (find_result, session["user_id"]))
                    datab.commit()

        return redirect("plan.html")

    else:
        return render_template("preferences.html")


@app.route("/plan", methods=["GET", "POST"])
@login_required
def plan():
    """Take the user to plan the trip"""

    if request.method == "POST":
        arrival = request.form["arrival"]
        departure = request.form["departure"]
        city = request.form["select_city"]

        # if both arrival, departure, and city were filled, then add them to the datab
        if city and arrival and departure:

            # count the amount of days
            first_day = datetime.datetime.strptime(arrival, "%Y-%m-%d")
            last_day = datetime.datetime.strptime(departure, "%Y-%m-%d")
            days = (last_day - first_day).days

            # add trip info into the table plans
            mycursor.execute("INSERT INTO plans (city, arrival, departure, days, id_user) VALUES (%s, %s, %s, %s, %s)", (city, arrival, departure, days, session["user_id"]))
            datab.commit()

            # get the id of the row just added to the table
            mycursor.execute("SELECT id FROM plans WHERE city=%s AND arrival=%s AND departure=%s AND id_user=%s", (city, arrival, departure, session["user_id"]))
            id_plan = mycursor.fetchone()[0]
            # print(id_plan)

            # get the cost_day from user_preferences table of the user
            mycursor.execute("SELECT cost_day FROM user_preferences WHERE id_user=%s", (session["user_id"],))
            convert_cost = mycursor.fetchone()[0]

            # convert the cost_day from integer to low, medium, or high so it's compatible with the places table price_level column
            if convert_cost <= 20:
                price_level = ("low")
            elif convert_cost >= 21 and convert_cost <= 70:
                price_level = ("medium")
            else:
                price_level = ("high")

            # for each day of the plan, select 4 places from the places table according to the chosen_categories table
            for day in range(days):
                mycursor.execute ("SELECT id FROM places WHERE city=%s AND price_level=%s AND id_cat IN (SELECT id_category FROM chosen_categories WHERE id_user=%s) ORDER BY RAND() LIMIT 4", (city, price_level, session["user_id"]))
                day = mycursor.fetchall()
                print(day)

                if len(day) == 4: 
                    # insert the places of each day into the days table
                    mycursor.execute("INSERT INTO days (id_plan, place_1, place_2, place_3, place_4) VALUES (%s, %s, %s, %s, %s)", (id_plan, day[0][0], day[1][0], day[2][0], day[3][0]))
                    datab.commit()

                elif len(day) == 3: 
                    # insert the places of each day into the days table
                    mycursor.execute("INSERT INTO days (id_plan, place_1, place_2, place_3) VALUES (%s, %s, %s, %s)", (id_plan, day[0][0], day[1][0], day[2][0]))
                    datab.commit()

                elif len(day) == 2:
                    # insert the places of each day into the days table
                    mycursor.execute("INSERT INTO days (id_plan, place_1, place_2) VALUES (%s, %s, %s)", (id_plan, day[0][0], day[1][0]))
                    datab.commit()

                else: 
                    # insert the places of each day into the days table
                    mycursor.execute("INSERT INTO days (id_plan, place_1) VALUES (%s, %s)", (id_plan, day[0][0]))
                    datab.commit()


            return redirect("/")
            # return ("it is working")
        
        else: # if any info is missing
            return apology("All fields are required")

    else:
        # check on the datab table if there is at least one row with the session user_id of the user logged in
        mycursor.execute("SELECT * FROM user_preferences WHERE id_user=%s", (session["user_id"],))
        result = mycursor.fetchone()

        # if there's no row with the session user_id logged in
        if not result:
            return redirect("/preferences")

        # if the user already filled in their preferences
        return render_template("plan.html")

@app.route("/")
@login_required
def index():
    """Your Trips - Display all the planned trips and old trips"""

    mycursor.execute("SELECT id, city, arrival, departure FROM plans WHERE id_user=%s",(session["user_id"],))
    trips_list = mycursor.fetchall()
 
    return render_template("index.html", trips_list=trips_list)



@app.route("/<trip_id>")
@login_required
def eachPlan(trip_id):
    """Display the plan of each trip"""

    mycursor.execute("""SELECT places.name, places.address
                    FROM (	
                    SELECT days.place_1
                    FROM days
                    WHERE id_plan 
                    IN (
                        SELECT id 
                        FROM plans 
                        WHERE id=%s
                        )
                    UNION ALL
                    SELECT days.place_2
                    FROM days
                    WHERE id_plan 
                    IN (
                        SELECT id 
                        FROM plans 
                        WHERE id=%s
                        )
                    UNION ALL
                    SELECT days.place_3
                    FROM days
                    WHERE id_plan 
                    IN (
                        SELECT id 
                        FROM plans 
                        WHERE id=%s
                        )
                    UNION ALL
                    SELECT days.place_4
                    FROM days
                    WHERE id_plan 
                    IN (
                        SELECT id 
                        FROM plans 
                        WHERE id=%s
                        ) 
                    ) AS temp 
                    INNER JOIN places ON places.id = temp.place_1""", (trip_id, trip_id, trip_id, trip_id))
    plan = mycursor.fetchall()

    mycursor.execute("SELECT city FROM plans WHERE id=%s", (trip_id,))
    city = mycursor.fetchone()

    return render_template("eachPlan.html", plan=plan, city=city[0])



