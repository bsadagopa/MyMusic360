from flask import Flask, render_template, redirect
import pandas as pd
import mm360_app as mm

app = Flask(__name__)

@app.route("/")
def home(): 
    # return template and data
    return render_template("Home.html")

@app.route("/get_started")
def get_started(): 
    # return template and data
    # return render_template("get_started.html")
    mm.from_web()

if __name__ == '__main__':
    app.run(debug=True)