#Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Creating Flask
app = Flask(__name__)

#Setting a variable for connection to Mongo DB
mongo = PyMongo(app, uri="mongodb://localhost:27017/nasa_app")

#Creating the "home" page with a function
@app.route("/")
def home():
    #Creating a variable for reflecting a docunt from Mongo DB
    mars_data = mongo.db.collection.find_one()

    #Setting the connection with html file
    return render_template("index.html", mars=mars_data)
    
#Creating "scrape" page with a function
@app.route("/scrape")
def scrape():
    #Setting a variable for imported from scrape_mars.py main function
    mars_data = scrape_mars.scrape_info()

    #Setting update existing Mongo DB document with a new information every time "scrapping" take place 
    mongo.db.collection.update({}, mars_data, upsert=True)

    #returning new scrapped information to the "home" page
    return redirect("/")

#Debug
if __name__ == "__main__":
    app.run(debug=True)