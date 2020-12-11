from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_costa


app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/nasa_app")


@app.route("/")
def home():

    

@app.route("/scrape")
def scrape():



if __name__ == "__main__":
    app.run(debug=True)