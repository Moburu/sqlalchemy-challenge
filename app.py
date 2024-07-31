# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/> "
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query the last 12 months of precipitation
    prcp_data = session.query(Measurement.prcp).filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()

    prcp_data = list(np.ravel(prcp_data))

    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    station_data = session.query(Station.station).all()

    station_data = list(np.ravel(station_data))

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281', Measurement.date.between('2016-08-23', '2018-08-23')).all()

    tobs_dicts = []
    for row in tobs_data:
        tobs_dicts.append({'date': row.date, 'tobs': row.tobs})

    return jsonify(tobs_dicts)

if __name__ == '__main__':
    app.run(debug=True)

session.close()
