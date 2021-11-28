#Imports
from flask import Flask, jsonify

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#connect to database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect tables as classes and save references
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask setup
app = Flask(__name__)


#####Flask routes
#Root route
@app.route("/")
def Home():
    return(
    f"Welcome to the Hawaii Weather API!<br/>"
    f"Available routes are:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/YYYY-MM-DD (from given date to end of data)<br/>"
    f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD (from given date to given date)<br/>"
    ) 


#All precipitation data
@app.route("/api/v1.0/precipitation")
def precip():
    #connect to db, query, and close connection
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).group_by(Measurement.date).all()
    session.close()
    
    #Convert the query results to a dictionary
    precip = []
    for date, prcp in results:
        day_dict = {}
        day_dict["Date"] = date
        day_dict["Precipitation"] = prcp
        precip.append(day_dict)

    #Return JSON representation
    return jsonify(precip)


#List of stations
@app.route("/api/v1.0/stations")
def stations():
    #connect to db, query, and close connection
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    
    #convert query result to list
    station_list = list(np.ravel(results))
    #Return a JSON list
    return jsonify(station_list)


#Temperature observations for the most active station for the previous year.
@app.route("/api/v1.0/tobs")
def temp():
    #calculate the dt variable for the last year of the dataset
    oneyearago = dt.date(2017,8,23) - dt.timedelta(days=365)

    #connect to db, query, and close connection
    session = Session(engine)
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= oneyearago).group_by(Measurement.date).all()
    session.close()

    #convert query result to list
    temp_list = list(np.ravel(results))
     #Return a JSON list
    return jsonify(temp_list)


#Temperature MIN, AVG, and MAX for all dates >= to the start date.
@app.route("/api/v1.0/<start>")
def startonly(start):   
    #connect to db, query, and close connection
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).first()
    session.close()
    
    #convert query result to list
    temp_stats = list(np.ravel(results))
    #Return a JSON list
    return jsonify(temp_stats)


#Temperature MIN, AVG, and MAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    #connect to db, query, and close connection
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).first()
    session.close()

    #convert query result to list
    temp_stats = list(np.ravel(results))
    #Return a JSON list
    return jsonify(temp_stats)


if __name__ == "__main__":
    app.run(debug=True)