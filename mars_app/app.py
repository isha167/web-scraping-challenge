from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Connect to PyMongo DB
client = pymongo.MongoClient('mongodb://localhost:27017')

# Connect to a database. Will create one if not already available.
db = client.mars_db

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database/***
    mars_dict = db.mars_dict.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_dict)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_dict = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    db.temps.update({}, mars_dict, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
   app.run(debug=True)

