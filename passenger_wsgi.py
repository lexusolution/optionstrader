import os
import sys


sys.path.insert(0, os.path.dirname(__file__))

# Import your Flask app
from app import app as application

# This makes your Flask app work with Passenger/your web server
if __name__ == "__main__":
    application.run() 

