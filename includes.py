from datetime import datetime
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, DateTime, CHAR, Identity, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
txtline= "============================================================"

def TechnoShedHelp(tsdappname,tsdappver):
    print("\n\n"+txtline+"\n"+tsdappname+"\nVersion\t"+str(tsdappver)+"\n"+txtline)
def makeconnection(serverdb,dbuser,dbpass): # Make connection to DB and RETURN the session
    serverhost = "technoshed.duckdns.org"
    connectionstring = "mysql+pymysql://"+dbuser+":"+dbpass+"@"+str(serverhost)+"/"+str(serverdb)
    engine= create_engine(str(connectionstring))
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
def loadvehicle(searchreg):             # takes GLOBAL session from makeconnection() and loads vehicle from DB into a Vehicle object
    searchreg = searchreg.upper()
    print("Searching REG      \t"+searchreg)
    if len(searchreg) >7:
        searchreg="TooLONG"
    session=makeconnection(serverdb="VehicleComments",dbuser="vehicleapps",dbpass="TsDvEhIcLeApPs")
    loadedvehicle = session.query(Vehicle).filter(Vehicle.reg == searchreg).first()
    if not loadedvehicle:
        print("               \t"+searchreg+" NOT FOUND")
        loadedvehicle = Vehicle(searchreg,"Not Found","Not Found","Invisible",0,0,"ZERO","Imagination","Nobody")
    else:
        print("Loaded REG      \t"+loadedvehicle.reg+" ("+loadedvehicle.make+" "+loadedvehicle.model+") with "+str(loadedvehicle.mileage)+"mls")
    return loadedvehicle


if __name__ == "__main__":

    TechnoShedHelp("Technoshed SQLalchemy and data processiong Functions\nThis is a LOCAL repository for LOCAL people!\nThere's NOTHING for YOU here!","")