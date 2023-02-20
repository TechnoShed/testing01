from includes import *
from flask import Flask

app = Flask(__name__)



@app.route('/')
def hello():
    return "<h1>\nHello, World!</h1>"

print(txtline+"\nhi\n"+txtline)

session = makeconnection("VehicleComments","vehicleapps","TsDvEhIcLeApPs")

app.run()
