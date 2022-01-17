"""
database.py
Handles database operations with a SQLITE database
All validation is done in server.py, not here
"""

import os
import sqlite3
from dotenv import load_dotenv

class Database:

    # Intializes the database handler
    # Connects to DB, verifies schema has been configured, if not, it calls initDB()
    def __init__(self):

        load_dotenv()
        self.db = os.getenv("DB_PATH") or "wolserver.db"

        con = sqlite3.connect(self.db)
        cur = con.cursor()

        # If DB has not been initialized (no tables exist), run initDB()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        if (len(cur.fetchall()) == 0):
            self.initDB()

        con.commit()
        cur.close()
        
    
    # Initialize database. Call this method if schema has not been generated or DB needs to be repaired
    # WARNING: will destroy any content currently in the DB
    def initDB(self):
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        cur.execute(""" DROP TABLE IF EXISTS devices """)
        cur.execute(""" CREATE TABLE devices (deviceID text, displayName text, macAddress text) """)

        con.commit()
        con.close()

    # Returns all data from devices table
    def getAllDevices(self):
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        cur.execute(""" SELECT * FROM devices ORDER BY displayName """)

        res = cur.fetchall()
        con.close()

        return res

    # Add a device to devices table
    def addDevice(self, deviceID, displayName, macAddress):
        device = (deviceID, displayName, macAddress)

        con = sqlite3.connect(self.db)
        cur = con.cursor()

        cur.execute(""" INSERT INTO devices values (?, ?, ?) """, (device))

        con.commit()
        con.close()

    # Remove device from devices table
    def removeDevice(self, deviceID):
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        cur.execute(""" DELETE FROM devices WHERE deviceID = ? """, (deviceID, ))

        con.commit()
        con.close()

    # Gets information about a specific device ID from devices table
    def getDeviceInfo(self, deviceID):
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        cur.execute(""" SELECT * FROM devices WHERE deviceID = ? """, (deviceID, ))

        res = cur.fetchall()
        con.close()

        return res

    # Checks if mac address already exists in DB, returns True if yes, False if no
    def isMacAddressInDB(self, macAddress):
        con = sqlite3.connect(self.db)
        cur = con.cursor()

        cur.execute(""" SELECT * FROM devices WHERE macAddress = ? """, (macAddress, ))

        if (len(cur.fetchall()) == 0): # No resulting rows, so item does not exist in DB
            con.close()
            return False
        else:
            con.close()
            return True

"""
# Test
db = Database()
db.initDB()

print("all devices:")
print(db.getAllDevices())
print()

print("adding device")
db.addDevice("id", "bens computer", "335")
print()

print("showing all: ")
print(db.getAllDevices())
print()

print("adding 2 more devices")
db.addDevice("id1", "bens computer", "335")
db.addDevice("id2", "bens computer", "335")
print()

print("showing all")
print(db.getAllDevices())
print()

print("removing last device 'id2'")
db.removeDevice("id2")
print()

print("showing all devices after removinglast one")
print(db.getAllDevices())
print()

print("showing info about id1")
print(db.getDeviceInfo("id1"))
"""