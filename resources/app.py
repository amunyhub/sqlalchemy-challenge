import numpy as np
from flask import Flask, jsonify
import pandas as pd
from flask import Flask, jsonify, Response
from flask_cors import CORS
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

# Flask Setup
#################################################
app = Flask(__name__)
# CORS(app)
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save a reference to the invoices table as `Invoices`
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (

        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/date/yyyy-mm-dd<br/>"
        f"/api/v1.0/date/yyyy-mm-dd/yyyy-mm-dd"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    # last day from jupyter notebook 
    year_recent = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    """Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    Return the JSON representation of your dictionary."""
    results = session.query(measurement.date, measurement.prcp, func.avg(measurement.prcp)).filter(
        measurement.date >= year_recent).group_by(measurement.date).all()
    session.close
    return jsonify(precipitation=results)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a JSON list of stations from the dataset."""
    stations = session.query(station.station).all()
    session.close
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    """Query the dates and temperature observations of the most active station for the last year of data.
    Return a JSON list of temperature observations (TOBS) for the previous year."""
    year_recent = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.tobs).filter(
        measurement.station == 'USC00519281').filter(measurement.date >= year_recent).all()
    session.close
    return jsonify(tobs=results)

@app.route("/api/v1.0/date/<start>")
@app.route("/api/v1.0/date/<start>/<end>")
def sttenddates(start=None, end=None):
    session = Session(engine)
    """* Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    * When given the start only or the start/end date, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date."""
    # SELECT Statement
    sel = [func.min(measurement.tobs), func.avg(
        measurement.tobs), func.max(measurement.tobs)]
    print("======================")
    print(*sel)
    print("======================")
    if not end:
        # calculate min, max, avg for dates greater than start
        # results = session.query(*sel).filter(measurement.date >= start).all()
        results = session.query(func.min(measurement.tobs), func.avg(
            measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    else:
        # calculate min, max, avg for dates between start and stop
        results = session.query(
            func.min(measurement.tobs), func.avg(
                measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    # unravel results into a 1D array and convert to list (array)
    temps = list(np.ravel(results))
    session.close
    return jsonify(temps=temps)
   
#     session.close()

#     country_data = []
#     for country, country_id, region in results:
#         nation_dict = {}
#         nation_dict["country_id"] = country_id
#         nation_dict["region"] = region
#         nation_dict["country"] = country
#         country_data.append(nation_dict)
# #     country_data = []
# #     for country, country_id, region in results:
# #         nation_dict = {}
# #         nation_dict["country_id"] = country_id
# #         nation_dict["region"] = region
# #         nation_dict["country"] = country
# #         country_data.append(nation_dict)

#     return jsonify(country_data)
# #     return jsonify(country_data)


#     # return jsonify(country_names) OLD DO NOT USE
# # @app.route("/api/v1.0/happiness_db/happiness_data")
# # def happiness_func():
# #     """Return the happiness_db data as json"""
# # #     # return jsonify(country_names)
# # @app.route("/api/v1.0/happiness_db/happiness_data")
# # def happiness_func():
# #     """Return the happiness_db data as json"""

#     # Create our session (link) from Python to the DB
#     session = Session(engine)
# #     # Create our session (link) from Python to the DB
# #     session = Session(engine)

#     """Return a list of all passenger names"""
#     # Query all passengers
#     results = session.query(happiness_data.happy_id, happiness_data.year, happiness_data.country_id, happiness_data.happiness_score, happiness_data.gdp, happiness_data.life_expectancy, happiness_data.freedom_score, happiness_data.trust_score, happiness_data.generosity_score).all()
# #     """Return a list of all passenger names"""
# #     # Query all passengers
# #     results = session.query(happiness_data.happy_id, happiness_data.year, happiness_data.country_id, happiness_data.happiness_score, happiness_data.gdp, happiness_data.life_expectancy, happiness_data.freedom_score, happiness_data.trust_score, happiness_data.generosity_score).all()

#     session.close()
# #     session.close()

#     # Convert list of tuples into normal list
#     happiness_dict = []
#     for happy_id, year, country_id, happiness_score, gdp, life_expectancy, freedom_score, trust_score, generosity_score in results:
#         happy_dict = {}
#         happy_dict["happy_id"] = happy_id
#         happy_dict["year"] = year
#         happy_dict["country_id"] = country_id
#         happy_dict["happiness_score"] = happiness_score
#         happy_dict["gdp"] = gdp
#         happy_dict["life_expectancy"] = life_expectancy
#         happy_dict["freedom_score"] = freedom_score
#         happy_dict["trust_score"] = trust_score
#         happy_dict["generosity_score"] = generosity_score
#         happiness_dict.append(happy_dict)
# #     # Convert list of tuples into normal list
# #     happiness_dict = []
# #     for happy_id, year, country_id, happiness_score, gdp, life_expectancy, freedom_score, trust_score, generosity_score in results:
# #         happy_dict = {}
# #         happy_dict["happy_id"] = happy_id
# #         happy_dict["year"] = year
# #         happy_dict["country_id"] = country_id
# #         happy_dict["happiness_score"] = happiness_score
# #         happy_dict["gdp"] = gdp
# #         happy_dict["life_expectancy"] = life_expectancy
# #         happy_dict["freedom_score"] = freedom_score
# #         happy_dict["trust_score"] = trust_score
# #         happy_dict["generosity_score"] = generosity_score
# #         happiness_dict.append(happy_dict)

#     return jsonify(happiness_dict)
# #     return jsonify(happiness_dict)


# # @app.route("/")
# # def welcome():
# #     return (
# #         f"Welcome to the Justice League API!<br/>"
# #         f"Available Routes:<br/>"
# #         f"/api/v1.0/justice-league"
# #     )

# # THIS IS THE REAL ROUTEEEEEEE
# @app.route("/api/v1.0/happiness")
# def happiness(): 
#     # session = Session(engine)

#     """Return a list of all passenger names"""
#     # Query all passengers
#     # results = session.query(happiness_data.happy_id, happiness_data.year, happiness_data.country_id,    
#     #     happiness_data.happiness_score, happiness_data.gdp, happiness_data.life_expectancy, 
#     #     happiness_data.freedom_score, happiness_data.trust_score, happiness_data.generosity_score,
#     #         countries.country, countries.country_id, countries.region).filter(
#     #         happiness_data.country_id == countries.country_id
#     #     ).all()
#     happiness_df = pd.read_sql('SELECT * FROM happiness_data', engine)
#     countries_df = pd.read_sql('SELECT * FROM country', engine)
#     joined_df = pd.merge(happiness_df, countries_df, on = "country_id")
#     print(len(joined_df))
#     print(len(happiness_df))
#     print(len(countries_df))

    # session.close()
    # return Response(joined_df.to_json(orient = "records"),mimetype="application/json")

if __name__ == "__main__":
    app.run(debug=True,port=5000)