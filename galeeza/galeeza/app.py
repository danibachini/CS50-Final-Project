# read https://www.loekvandenouweland.com/content/full-path-in-zsh-shell.html

import mysql.connector
from bcrypt import hashpw, checkpw, gensalt
# from flask import Flask, flash, redirect, render_template, request, session

# How to use bcrypt: 
# https://blog.carsonevans.ca/2020/08/02/storing-passwords-in-flask/ 
# https://www.npmjs.com/package/bcrypt?activeTab=readme


db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Thg489!asf",
    database="galeeza"
)


# check how difficult is django - compared to flask




