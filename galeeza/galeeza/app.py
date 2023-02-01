# read https://www.loekvandenouweland.com/content/full-path-in-zsh-shell.html

# How to use bcrypt: 
# https://blog.carsonevans.ca/2020/08/02/storing-passwords-in-flask/ 
# https://www.npmjs.com/package/bcrypt?activeTab=readme

import sys
import mysql.connector
from bcrypt import hashpw, checkpw, gensalt
from flask import Flask, flash, redirect, render_template, request, session

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask"


db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Thg489!asf",
    database="galeeza"
)



# FLASK AND BCRYPT NOT WORKING
# https://stackoverflow.com/questions/71277049/import-could-not-be-resolved-pylancereportmissingimports
# https://stackoverflow.com/questions/52581576/could-not-import-d-flask-app