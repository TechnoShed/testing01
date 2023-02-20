from datetime import datetime
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, DateTime, CHAR, Identity, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()

class Vehicle(Base):
    __tablename__ = "vehicles"

    reg = Column("reg", String(7), unique=True, primary_key=True)
    make = Column("make",String(15), nullable=False)
    model = Column("model",String(15), nullable=False)
    colour = Column("colour",String(10), nullable=False)
    mileage = Column("mileage",Integer, nullable=False)
    year = Column("year",Integer, nullable=False)
    status = Column("status", String(4), nullable=False)
    site = Column("site",String(10), nullable=False)
    updatedby = Column("updatedby", String(20), nullable=False)
    updatedon = Column("updatedon",DateTime, default=datetime.utcnow())
    def __init__(self, reg, make, model, colour, mileage, year, status, site, updatedby):
        self.reg = reg.upper()
        self.make = make
        self.model = model
        self.colour = colour
        self.mileage = mileage
        self.year = year
        self.status = status
        self.site = site
        self.updatedby = updatedby
    def __repr__(self):
        return f"({self.reg}) {self.year} {self.colour} {self.make} {self.model} with Mileage {self.mileage} at Status {self.status} at {self.site} Last updated ({self.updatedby} on {self.updatedon})"
    def addComment(self, commenttoadd, commentuser):
        if commenttoadd == "":
            return
        else:
            newcomment = Comment(comment=commenttoadd,commentby=commentuser,reg=self.reg)
            newcomment.commenton=datetime.utcnow()
            session.add(newcomment)
            session.commit()
            self.updatedby = "Comment #"+str(newcomment.commentid)
            self.update()
    def getComments(self):
        session = makeconnection("VehicleComments","vehicleapps","TsDvEhIcLeApPs")
        foundcomments = session.query(Comment).filter(Comment.reg == self.reg).order_by(Comment.commenton.desc())
        if not foundcomments:
            print("ERROR : No inspections for vehicle "+self.reg)
        else:
            return foundcomments
    def update(self):
        self.updatedon=datetime.utcnow()
        session.commit()
    def markBad(self):
        self.addComment("Marked UNSAFE","Status Change ")
        self.status="DNU"
        self.update()
    def markSafe(self):
        self.addComment("Marked SAFE","Status Change ")
        self.status="OKAY"
        self.update()
    def markOffsite(self):
        self.addComment("Marked OFFSITE","Status Change ")
        self.status="AWAY"
        self.update()
    def markOnsite(self):
        self.addComment("Marked ONSITE","Status Change ")
        self.status="OKAY"
        self.update()
    def updateMileage(self, newmileage):
        oldmileage = int(self.mileage)
        newmileage = int(newmileage)
        if (newmileage - oldmileage)< 1 :
            print("ERROR : Mileage must be greater than current mileage")
        else:
            self.mileage = newmileage
            self.addComment(str(self.mileage-oldmileage)+" mls added from "+str(oldmileage)+" to "+str(self.mileage),"Mileage Update")
            self.updatedby = "Mileage Update"
            self.update()
            print("Updated Mileage     \t"+self.reg+" added "+str(self.mileage-oldmileage)+" mls added from "+str(oldmileage)+" to "+str(self.mileage))
    def updateSite(self, newsite):
        if newsite == self.site:
            return
        else:
            self.addComment("Site Changed from "+self.site+" to "+newsite, "Site Update   ")
            self.site= newsite
            self.updatedby="Site Update   "
            self.update()
class Comment(Base):
    __tablename__ = "comments"

    commentid = Column("commentid", Integer,primary_key=True)
    comment = Column("comment",String(128), nullable=False)
    commentby = Column("commentby",String(20), nullable=False)
    commenton = Column("commenton",DateTime, default=datetime.utcnow())
    reg = Column(String(7), ForeignKey(Vehicle.reg))
    
    # def __init__(self, commentid, comment, commentby, commenton, reg):
    def __init__(self, comment, commentby, reg):
        #self.commentid = commentid
        self.reg = reg
        self.comment = comment
        self.commentby = commentby
        #self.commenton = commenton
    def __repr__(self):
        return "("+self.commentid+") on "+str(self.reg)+" at "+str(self.updatedon)+" by "+self.updatedby+" :\t"+self.comment
