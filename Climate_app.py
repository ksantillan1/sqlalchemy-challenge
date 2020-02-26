# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#Import dependencies
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from flask import Flask, jsonify
import numpy as np

#Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


#Reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)


#Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


#Flask Setup
app = Flask(__name__)


@app.route("/")

#List all routes that are available.

def Home():
   
    return (
        f"Available Routes:<br/>"
        
        f"/api/v1.0/precipitation <br/>"

        f"/api/v1.0/stations <br/>"

        f"/api/v1.0/tobs <br/>"

        f"/api/v1.0/&ltstart&gt <br/> "
                
        f"/api/v1.0/&ltstart&gt/&ltend&gt <br/>"
    )

@app.route("/api/v1.0/precipitation")

def precipitation():
    
    #Convert the query results to a Dictionary using `date` as the key and `prcp` as the value
    
    session = Session(engine)
    
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    query_12month = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)
   
    Dataquery = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=query_12month).order_by(Measurement.date).all()
    
    session.close()

    #Return the JSON representation of your dictionary
    
    DataqueryList = []
    for data in Dataquery:
        data_dict = {}
        data_dict["date"] = data[0]
        data_dict["precipitation"] = data[1]
        DataqueryList.append(data_dict)
  
    return jsonify(DataqueryList)
 

@app.route("/api/v1.0/stations")

def stations():  
    
    #Return a JSON list of stations from the dataset
    session = Session(engine)
    
    Stations = session.query(Station.station, Station.name).all()
    session.close()
    
    station_list = list(np.ravel(Stations))
    return jsonify(station_list)
    

@app.route("/api/v1.0/tobs")

def tobs():

    
    #query for the dates and temperature observations from a year from the last data point.
    session = Session(engine)
    
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    query_12month = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    Obs_query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>=query_12month).all()
    
    session.close()
    
    #Return a JSON list of Temperature Observations (tobs) for the previous year
    
    ObsList = []
    for obs in Obs_query:
        obs_dict = {}
        obs_dict["Temperature"] = obs[1]
        
        ObsList.append(obs_dict)
  
    return jsonify(ObsList)
    


@app.route("/api/v1.0/<start>")

#When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

def calc_temps_start(start_date):
    
    session = Session(engine)
    Temp_stats1 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    session.close()
    
    Temp_stats_list1 = list(np.ravel(Temp_stats1))
    return jsonify(Temp_stats_list1)
    


@app.route("/api/v1.0/<start>/<end>")

#When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

def calc_temps(start_date, end_date):
    
    session = Session(engine)
    Temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
    
    Temp_stats_list = list(np.ravel(Temp_stats))
    return jsonify(Temp_stats_list)


if __name__ == '__main__':
    app.run()