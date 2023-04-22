

--------------->>>>>> clone project to codespace to submit it <<<<<<<-------------- 

# Trip Planner
#### Video Demo:  <URL HERE>
#### Description:


### The Platform

Galeeza is an automated and personalised trip planner. The user creates an account and fills his preferences. 
Once the preferences were informed, the user is allowed to plan as many trips as he wishes. In the database 
we count with information of places from 6 cities: 

- Paris, 
- New York City, 
- Barcelona, 
- Rome, 
- Berlin, 
- Tokyo. 

Therefore, the user has to select one of those cities (in a dropdown button) and pick the dates of his trip. 
Those places are divided into two types: they are either attractions or restaurants. In the attraction type,
we can find the following categories: 

- tourism and view sights, 
- museums, 
- sports, 
- music, 
- shopping, 
- parks and nature, 
- group activities, 
- kids activities, 
- night (bars, pubs, and night clubs), 
- religion (to visit religious places like cathedrals). 

In the restaurant type, we can find the following categories:  

- steakhouse, 
- sea food, 
- dietary, 
- vegetarian and vegan, 
- pizza and pasta, 
- fast food, 
- regional food, 
- cafe.

Once the planning of the trip was created automatically according to the user preferences, the trip planning is 
displayed in the page 'Your Trips' (which is also the index of the webapp). In the page 'Your Trips' the user
can see the old and the coming trips. In this page the user sees a list of the trips, identified by the name of
the city and the dates. To check the planning of a certain trip, the user clicks on the button 'See Plan'. He is
then redirected to the page displaying all the places to visit according to the his preferences and amount of 
days he will spend in the destination. 


### The Dev Toolset

For the development of this webapp, it was used the following toolset: 

- Python 
- Javascript
- Flask
- Jinja
- HTML
- CSS
- Bootstrap
- MySQL
- Poetry
- Git
- GitHub


### The Code

#### HTML

For the HTML templates, we have the following:

- layout.html: it defines the overall structure and styling of the webapp. It includes a navbar that changes 
depending on whether the user is logged in or not. Before the user is logged in, the navbar contains only a 
link to the 'Log in' page and a link to the 'Sign Up' page. Once the user is logged in, the navbar links 
change to the 'Your Trips' page, 'Plan a Trip' page, and a 'Log Out' button. It also includes a main content 
section that is meant to be populated by individual page templates that extend this layout template. At the 
bottom of the page, there is a footer that displays the copyright information for the application. The 
layout template includes links to necessary CSS and JavaScript files, including Bootstrap CSS and JS, as well 
as the application's own custom styles.

- signup.html: the 'Sign Up' page contains the logo of the brand and 5 fields: First Name, Last Name, Email, 
Password, and Password Confirmation. All fields are required in order for the user to create an account. 
Below the 5 fields to fill in the information, there is a button 'Sign Up for Free' which will sign up
the user if all the fields were correctly filled in. 

- login.html: the 'Log In' page contains 2 fields: Email and Password. These information have to be exactly 
the same provided by the user when he created his account. Right below the fields, there is a button written 
'Log In'. 

- index.html: once the user signs up or logs in, he is directed to the index page. In the case where the user
just created an account, the 'Index' page is empty, but if the user logs in and has previously planned one or
more trips, he will see all his trips displayed on this page. The 'Index' page shows a list of trips, old ones
and coming ones, and each trip plan can be identified by the 3 information given: name of the city, and both
arrival and departure dates. Also, by the side of each trip, there is a button written 'See Plan'. Once the user 
finds the trip he wants to check the planning, he clicks on the button and is then redirected to the page 
with the trip planning of that city and dates. 

- eachPlan.html: in this page we can see the specific planning of the trip selected in the 'Index' page. Here
the user will check the name and address of the places he is planned to visit according to the amoung of days
his trip is going to last. For each day, the user will receive an amount of 4 places to go (both attractions
and restaurants). So if the trip is going to last 3 days, the user will see in the 'eachPlan' page a total of
12 places divided into 3 blocks representing each day. At the top of the block the user can read 'Day' and its
respective number of the order of the days (Day 1, Day 2, and so on) followed by the name of the places and their
addresses. All places in the planning were automatically selected according to the preferences of the user. So, 
for example, if the user selected 'museums' and 'sea food' restaurants in his preferences, he will see places 
that are categorized as museums and sea food restaurants in his planning. 

- preferences.html: when the user clicks on the link 'Plan a Trip' in the navbar, if the user has not yet informed
his preferences, he will be redirected to the 'Preferences' page. The 'Preferences' page has a multiple-step form. 
The  first question is 'What's your favorite type of thing?' followed by 10 options which the user can select as 
many as he wishes. The options of the first question are 'Tourism / View sights', 'Museums', 'Sports / Adventure', 
'Music', 'Shopping', 'Parks / Nature', 'Group Activities', 'Kids Activities', 'Night Life', and 'Religion'. 
Once the user has selected all the option that are compatible with his own preferencces, the user then clicks
on the 'Next' button so he can see the next question. The second question asks 'What's the limit for spending per 
day?' followed by a range that starts with zero dollars ($0) and ends with a hundred dollars ($100). The
range is automatically set to fifty dollars ($50) and the user can run the range button left or right to 
decrease or increase the amount of cost per day. Once the user has selected the amount of money he is willing 
to spend per day, he then clicks the 'Next' button to go to the next question. The third question asks 'What's 
your favorite type of food?' followed by 6 options in which the user can select as many as he wishes. The options 
are 'Steakhouse', 'Sea Food', 'Dietary / Clean Eating', 'Vegetarian / Vegan', 'Pizza / Pasta', 'Fast Food', 
'Regional Food', and 'Cafe'. Once the user has selected all the option according to his own preferences, he
then clicks on the 'Next' button taking him to the confirmation section with the message 'Now you're ready 
to go! Your profile is ready to start planning your trip!'. Below the text there is the 'Plan Your Trip' 
button that takes him to the 'Plan a Trip' page. During the whole process, except for the first question, 
the user has a 'Previous' button below the questions so he can come back to the previous question to edit
it.

- plan.html: in the 'Plan a Trip' page, at the top of the page the user reads 'Select the destination and 
dates of your trip' followed by 3 dropdown buttons. The first dropdown button contains a list of 6 cities 
to choose. The cities are 'Paris', 'New York City', 'Barcelona', 'Rome' 'Berlin', and 'Tokyo'. Once the
user has selected the city he is traveling to, he then selects the dates. The second dropdown button 
refers to the arrival date in the city and the third dropdown button refers to the departure date. 
When the user clicks on those arrival and departure dropdown buttons, he sees a calendar where he can choose
the year, month, and day. The calendar starts with the current day and once the user has selected the arrival
date in the city, for the departure date he only has available the dates after the arrival date (as you cannot 
leave a place before arriving there). Once all filds were answered (they are all required), the user 
clicks on the 'Submit' button and is then redirected to the 'Index' page where he can check his trip planing. 

- apology.html: the 'Apology' page displays an image using a custom URL generated by the 'memegen.link' service. 
The top and bottom variables in the URL are filled with user-provided strings using the {{ top }} and {{ bottom }} 
Jinja2 template variables respectively. The 'Apology' page is displayed when the user does something wrong or not 
supposed to be done, like trying to create a password without all of its requirements or not filling mandatory fields. 


#### JavaScript

For JavaScript, we have the following:

- scriptPref.js: this file is used in the preferences.html file to handle the multiple-step preferences form. It 
allows the user to move between different sections of the form and submit his preferences. It stores the values 
selected in checkboxes and sends them to the server using an AJAX request. It also replaces the URL once the 
form is submitted so that the user cannot go back to the form again and it handles the range input.

- scriptPlan.js: this file controls the form in the plan.html file. When the user selects a city in the dropdown 
button, the text of the button is updated to match the selected city. When the user selects a new date for the 
arrival, the minimum value of the departure input is automatically updated to be the same as the selected by the 
user. Then, when the user selects the date for the departure, the maximum value of the arrival input is updated 
to be the same as the selected by the user for the departure date.


#### Python

For Python, we have the following:

- app.py: the app.py file is divided into 7 '@app.route' parts. 

    - @app.route("/signup", methods=["GET", "POST"]): the first refers to the 'Sign Up' page and it renders the 
    signup.html file. It checks if all fields were filled in and if the information input in the fields are 
    correct. So first the code checks if there is an existing email in the database comparing with the email 
    provided by the user. If there is already an account with the email provided, it displays the 'Apology' page 
    to the user informing him about it and the account is not created. If the email provided does not exist in 
    the database, the code then checks the following constraints about the inputs: if any field is empty, if 
    password does not match password  confirmation, and if password is longer than 8 characters and contains 
    both lower and uppercase. If any of those info were not correctly provided, the webapp displays the 'Apology' 
    page. If all requirements were met, then the password is hashed and salted using bcrypt and all the information 
    is added to the database. Finally, once all  the info about the users is stored, the user is automatically 
    redirected to the 'Index' page. 

    - @app.route("/login", methods=["GET", "POST"]): here the first step is to make sure that the session is
    clear so the user can log in. The GET method returns the login.html file, and once the user has filled in 
    email and password, the code first checks if either or both fields were properly filled, otherwise the user
    gets the 'Apology' page. Secondly, it checks if email and password match with the data stored in the database. 
    If they do not match, the user gets the 'Apology' page. Once everything is cleared up, the user id is added to
    the session in order to remember the user who is logged and it redirects the user to the 'Index' page. 

    - @app.route("/logout", methods=["GET", "POST"]): it logs the user out by clearing the session. 

    - @app.route("/preferences", methods=["GET", "POST"]): it requires login to access the 'Preferences' page. 
    The GET method renders the preferences.html with the multiple-step form. Then, as the user hits the 'Next'
    button, information is added to the database. There is a check to see if the information coming is 
    numeric or not since the only numeric informationn coming from the form is the amount of money per day. 
    If the information is numeric, it is saved or updated to its own table in the database. If it is not 
    numeric, it means it is one of the categories selected and then, if it does not yet exist in the table with
    the user id, it is added. Once all preferences were answered, it redirects the user to the 'Plan' page. 

    - @app.route("/plan", methods=["GET", "POST"]): it requires login to access the 'Plan' page. It first 
    checks in the database if the user has answered the preferences. If he did not, then it takes the user 
    to the 'Preferences' page. Else, the user has access to the 'Plan' page, which renders the plan.html file.
    Here it colects the city, arrival, and departure info. All of the 3 must be filled in, otherwise it displays
    the 'Apology' page. If all are correct, then it counts the amount of days between arrival and departure - 
    this is important to understand the number of days the user will stay in the city and, therefore, in how
    many days the plan will be divided. The information is then added to the database. Since the cost per day 
    is given from $0 to $100, the cost is converted into low, medium, or high. This is useful since the places 
    in the database are tagged using the same price level structure rather than numbers. Once this is done, 
    there is a loop adding 4 places per day (using the number of days calculated previously) into the 
    database regarding this specific trip and user. Finally, after all places were already defined according
    to the preferences of the user and cost, the user is then redirected to the 'Index' page where he can check 
    what has been added to his plan. 

    - @app.route("/"): it requires login to access the 'Index' page. It renders index.html. Here the user sees all
    of his trip plans - old and future ones. It gets the city name and arrival and departure dates from the 
    database of all trips conected to the current user id and display them to the user.

    - @app.route("/<trip_id>"):  it requires login to access the trip page. It renders eachPlan.html. Here a query 
    is executed to select all the places names and addresses whose ids match the ids of the places in the user's 
    planning for the specific city the user selected. 




