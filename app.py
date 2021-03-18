import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

###################################
# Database Setup
###################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

###################################
# Flask Setup
###################################
app = Flask(__name__)

###################################
# Flask Routes
###################################

# Route 1 - Home Route

@app.route("/")
def index():
    """List all available api routes."""
    return(
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

# Route 2 - Precipitation Route

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_precipitation = []

    for date, prcp in results:
        measurement_dict = {}
        measurement_dict["date"] = date
        measurement_dict["prcp"] = prcp
        all_precipitation.append(measurement_dict)


    return jsonify(all_precipitation)

# Route 3 - Stations Route

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# Route 4 - Date and Temperature of Most Active Station Route    

@app.route("/api/v1.0/tobs")
def temperature():

    session = Session(engine)

    most_active_year = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2016-08-23').\
        order_by(Measurement.date.asc()).all()

    session.close()

    all_temperature = []

    for station, date, tobs in most_active_year:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_temperature.append(tobs_dict)

    return jsonify(all_temperature)

# Route 5 - Min, Max, and Average Temperatures from '2016-08-23' and Greater Route

@app.route("/api/v1.0/<start>")
def statistics(start=None):

    session = Session(engine)

    year_data = session.query((func.min(Measurement.tobs)), (func.max(Measurement.tobs)), (func.avg(Measurement.tobs))).\
        filter(Measurement.date >= start).all()

    session.close()

    all_statistics = list(np.ravel(year_data))
      
    return jsonify(all_statistics)
                        

# Route 6 - Min, Max, and Average Temperatures using a start and an end date.

@app.route("/api/v1.0/<start>/<end>")
def statistics2(start=None, end=None):

    session = Session(engine)

    year_data = session.query((func.min(Measurement.tobs)), (func.max(Measurement.tobs)), (func.avg(Measurement.tobs))).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    all_statistics = list(np.ravel(year_data))
      
    return jsonify(all_statistics)


if __name__ == '__main__':
    app.run(debug=True)
