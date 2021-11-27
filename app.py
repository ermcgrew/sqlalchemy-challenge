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

#Flask routes
@app.route("/")
def Home():
    return(
    f"Welcome to the Hawaii Weather API!<br/>"
    f"Available routes are:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/<start><br/>"
    f"/api/v1.0/<start>/<end><br/>"
    ) 


@app.route("/api/v1.0/precipitation")
def precip():
    #connect to db, query, and close connection
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).group_by(Measurement.date).all()
    session.close()
    
    #Convert the query results to a dictionary using date as the key and prcp as the value.
    precip = []
    for date, prcp in results:
        day_dict = {}
        day_dict["Date"] = date
        day_dict["Precipitation"] = prcp
        precip.append(day_dict)

    #Return JSON representation
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    #connect to db, query, and close connection
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    
    station_list = list(np.ravel(results))

    #Return a JSON list of stations from the dataset
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temp():
    session = Session(engine)
    #Query the dates and temperature observations of the most active station for the last year of data.
    oneyearago = dt.date(2017,8,23) - dt.timedelta(days=365) #max(Measurement.date)

    # busy_station = session.query(Measurement.station, func.count(Measurement.prcp)).\
    #     group_by(Measurement.station).order_by(func.count(Measurement.prcp).desc()).first()

    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= oneyearago).group_by(Measurement.date).all()
    
    session.close()

    temp_list = list(np.ravel(results))

    # Return a JSON list of temperature observations (TOBS) for the previous year. 
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def startonly():
    return
# Return a JSON list of the minimum temperature, 
# the average temperature, and the max temperature 
# for a given start or start-end range.

#calculate TMIN, TAVG, and TMAX for all dates 
# greater than and equal to the start date.

@app.route("/api/v1.0/<start>/<end>")
def startend():
    return
# Return a JSON list of the minimum temperature, 
# the average temperature, and the max temperature 
# for a given start or start-end range.

#When given the start and the end date, 
# calculate the TMIN, TAVG, and TMAX 
# for dates between the start and end date inclusive.



if __name__ == "__main__":
    app.run(debug=True)