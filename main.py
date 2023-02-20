from includes import *
from flask import Flask

app = Flask(__name__)



@app.route('/')
def hello():
    return 'Hello, World!'

print(txtline+"\nhi\n"+txtline)

session = makeconnection("VehicleComments","vehicleapps","TsDvEhIcLeApPs")

app.run()
