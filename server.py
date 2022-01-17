"""
server.py
---------
Main entry point of application. Contains routing logic
"""

from flask import Flask
from flask import render_template, request, url_for, flash, redirect, Response, jsonify

from dotenv import load_dotenv
load_dotenv()

import requests as rr
import re

from database import Database
db = Database()

app = Flask(__name__)
app.config["SECRET_KEY"] = "7e1f71d83e92ac615a431ad30cb8b650e528af7b04092e2d"

""" Routing """

# Index
@app.route("/")
def index():
    return render_template("index.html")

# Add a device
@app.route("/add-device", methods=("GET", "POST"))
def addDevice():

    if request.method == "POST":
        displayName = request.form["display-name"]
        macAddress = request.form["mac-address"]

        # Form validation
        if not displayName:
            flash("Display name required")
            
        elif len(displayName) > 20:
            flash("Display name must be 20 characters or less")
            
        
        elif not macAddress:
            flash("Mac address required")
            
        elif re.match("^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", macAddress) == None:
            flash("Mac address not formatted correctly. Format: XX-XX-XX-XX-XX-XX")
            
        elif db.isMacAddressInDB(macAddress):
            flash("Mac address already exists in database")

        # @TODO: more form validation...

        # Render success page
        else:
            # Add to DB
            id = macAddress # for simplicity's sake, device ID will just be the Mac Address
            db.addDevice(id, displayName, macAddress)

            return render_template("add_device__success.html")

    # GET request was made, or form had invalid data and we need to stay on form page
    return render_template("add_device.html")

# Remove device
@app.route("/remove-device")
def removeDevice():

    # If a URL parameter is provided (id), we are deleting a device
    if request.args.get("id"):

        # Send a POST to the endpoint
        macAddress = request.args.get("id")
 
        url = request.url_root + "/api/v1/remove-device?id=" + str(macAddress)
        req = rr.post(url)
        res = req.json()

        # Route based on API response
        if res.get("responseCode") == 200:
            return render_template("remove_device__success.html")
        else:
            return render_template("error.html", error=res)
    
    # If no URL parameter is provided, we load the device list
    else:
        deviceList = db.getAllDevices()
        return render_template("device_list__remove.html", devices=deviceList)

# Wake up device
@app.route("/wake-up")
def wakeUp():

    # If a URL parameter is provided (id), we are waking up a device
    if request.args.get("id"):
        
        macAddress = request.args.get("id") # Device ID is mac address
            
        url = request.url_root + "/api/v1/wake-up?id=" + str(macAddress)
        req = rr.post(url)
        res = req.json()

        # Route based on API response
        if res.get("responseCode") == 200:
            return render_template("device_wake__success.html")
        else:
           return render_template("error.html", error=res)    

    # If no URL parameter is provided, we load the device list
    else:
        deviceList = db.getAllDevices()

        return render_template("device_list__wake_up.html", devices=deviceList)

# Settings
@app.route("/settings")
def settings():
    return render_template("settings.html")

# About page
@app.route("/about")
def about():
    return render_template("about.html")

# Delete database
@app.route("/delete-database")
def deleteDatabase():
    db.initDB()
    return "Deleted DB"

"""
API Endpoints - These take POST requests, either sent over the network with local API key or through the application 
"""
# Wake a device up
# Paramters:
#   Mac Address
@app.route("/api/v1/wake-up", methods=["POST"])
def apiWake():
    
    if request.args.get("id"):
        deviceID = request.args.get("id")

        if db.isMacAddressInDB(deviceID):

            # @TODO wake on lan
            # @TODO wake on lan error handlign
            return jsonify( responseCode = 200 )
        
        else:
            return jsonify(
                responseCode = 500,
                errorMessage = "Mac address is not in database"
            )
    else:
        return jsonify(
                responseCode = 500,
                errorMessage = "No 'id' provided. Add an ?id=MAC_ADDRESS parameter to the end of your URL"
        )

# Removes a device from the database
@app.route("/api/v1/remove-device", methods=["POST"])
def apiRemove():

    if request.args.get("id"):
        deviceID = request.args.get("id")

        if db.isMacAddressInDB(deviceID):
            db.removeDevice(deviceID)
        
            return jsonify(
                responseCode = 200
            )

        else:
            return jsonify(
                responseCode = 500,
                errorMessage = "Mac address is not in database"
            ) 
    else:
        return jsonify(
            responseCode = 500,
            errorMessage = "No 'id' provided. Add an ?id=MAC_ADDRESS parameter to the end of your URL"
        )

# Run app
if __name__ == "__main__":

    # @TODO
    # if (env.debug) then debug else, no debug

    app.run(debug=True)