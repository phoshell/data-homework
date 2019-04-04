# 1. Import Flask
# Python SQL toolkit and Object Relational Mapper
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

# Create our session (link) from Python to the DB
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
session = Session(engine)

# Reflect Database into ORM classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# 2. Create an app
app = Flask(__name__)

# 3. Define static routes
@app.route("/")
def index():
    """list all API routes"""
    return (
        f"Welcome to my Hawaii trip info!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

prev_year = dt.date(2017,8,23) - dt.timedelta(365)

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a Dictionary using [date] as the key and [prcp] as the value."""
    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()

        # Create a dictionary from the row data and append to a list 
    precip_dict = {}
    for date, prcp in precip:
        if prcp !=None:
            precip_dict.setdefault(date, []).append(prcp)

    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    station_locs = session.query(Station.station).all()
    stations = list(np.ravel(station_locs))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    obs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= prev_year).all()
    obs_dict = {}
    for date, tobs in obs:
        if tobs !=None:
            obs_dict.setdefault(date, []).append(tobs)
            print("I don't have an END variable.")
    
    return jsonify(obs_dict)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def date(start=None, end=None):
    if not end:
        start_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
        start_sort = list(np.ravel(start_date))
        return jsonify(start_sort)
    else:
        end_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date <= end).all()
        end_sort = list(np.ravel(end_date))
        return jsonify(end_sort)

# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)