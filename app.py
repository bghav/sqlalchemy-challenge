import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# Flask Setup#################################################
app = Flask(__name__)

# Flask Routes#################################################
@app.route('/')
def Home():
    return (
        f"Welcome to Weather Data Api!<br/>"
        f"Available Routes<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route('/api/v1.0/precipitation')
def precipitation():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

   # """Return a list of precipitation data including the date and prcp"""
    # Query all precipitation
    dtp= session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date > '2016-08-22', Measurement.prcp).\
    order_by(Measurement.date.desc()).all()
    dtp

    session.close()
    # Create a dictionary from the row data and append to a list of precipitation
    all_prcp = []
    
    for date, prcp in dtp:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp  
        all_prcp.append(precipitation_dict)
    
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    act= session.query(Measurement.station).\
    group_by(Measurement.station).\
    order_by(Measurement.station.desc()).all()
    act

    session.close()
     # Convert list of tuples into normal list
    all_stations = list(np.ravel(act))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    tr = session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date > '2016-08-22').filter(Measurement.station == 'USC00519281').all()
    tr

    session.close()
     # Convert list of tuples into normal list
    all_tr = list(np.ravel(tr))

    return jsonify(all_tr)

if __name__ == '__main__':
    app.run()