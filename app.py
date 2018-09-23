# import necessary libraries
from flask import Flask, render_template, jsonify, redirect
import pymongo
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape"
mongo = PyMongo(app)

# create route that renders index.html template and finds documents from mongo
@app.route("/")
def index():
    # Find data using try/except - kept getting failures
    try:
        mars_data = mongo.db.mars_data.find_one()
        return render_template('index.html', mars_data=mars_data)
    except:
        # return template and data
        return redirect("http://localhost:5000/scrape", code=302)

# Route that will trigger scrape functions
@app.route("/scrape")
def scraped():
    # Run scraped functions
    mars_data = mongo.db.mars_data
    mars_data_scrape = scrape_mars.scrape()

    # Update Mars scrape data into database
    mars_data.update(
        {},
        mars_data_scrape,
        upsert=True
    )
    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

    # Notes - used Week 3 instructor 'scrape_and_render' and student 'scrape_weather' activities plus other references found on GitHub to get this code to execute properly.