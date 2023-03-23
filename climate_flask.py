import os
import sqlite3
import datetime as dt
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#now the flask set up
app = Flask(__name__)

#setting up the data base just like the first half of homework
engine= create_engine ("sqlite:///Resources/hawaii.sqlite")
Base= automap_base()
Base.prepare(autoload_with=engine)

measurement=Base.classes.measurement
station=Base.classes.station

session=Session(engine)



#routing flask
@app.route("/")
def welcome():
    return (
        f"Hawaii Climate Analysis<br/>"
        f"Routes Available for this Analysis<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year=dt.date(2017,8,23)- dt.timedelta(days=365)
    precipitation=session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= last_year).all()
    session.close()
    prec={date:prcp for date, prcp in precipitation}
    return jsonify(prec)


@app.route("/api/v1.0/stations")
def stations ():
    last_year=dt.date(2017,8,23)- dt.timedelta(days=365)
    scores=session.query(measurement.tobs).\
        filter(measurement.station== 'USC00519281').\
        filter(measurement.date >= last_year).all()
    
    session.close()
    stations=list(np.ravel(scores))
    return jsonify (stations)


@app.route("/api/v1.0/tobs")
def temp_obs():
    last_year=dt.date(2017,8,23)- dt.timedelta(days=365)
    scores=session.query(measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= last_year).all()
    session.close()

    temperature=list(np.ravel(scores))
    return jsonify(temperature)

@app.route("/api/v1.0/temp/start")
def tem(start):
    begin_date=dt.datetime.strptime(start, "%m%d%y")
    last_year=dt.timedelta(days=365)
    start=begin_date-last_year
    end=dt.date(2017,8,23)
    stat=session.query(func.min(measurement.tobs), func.avg(measurement.tobs),func.max(measurement.tobs)).\
        filter(measurement.date>=start).filter(measurement.date <= end).all()
    session.close()
    data=list(np.ravel(stat))
    return jsonify(data)

@app.route("/api/v1.0/temp/start/end")
def temp(start,end):
    begin_date=dt.datetime.strptime(start, "%m%d%y")
    end_date=dt.datetime.strptime(end, "%m%d%y")
    last_year=dt.timedelta(days=365)
    start=begin_date-last_year
    end=end_date-last_year
    stat=session.query(func.min(measurement.tobs), func.avg(measurement.tobs),func.max(measurement.tobs)).\
        filter(measurement.date>=start).filter(measurement.date <= end).all()
    session.close()
    data=list(np.ravel(stat))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)