from flask import Flask, render_template
import pandas as pd


app = Flask("Website")

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]
# adding the stations on the home page so that user can see all the possible stations


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>")
def all_data(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    # if not for orient="records" it brakes the data and they look awful
    return result


@app.route("/api/v1/yearly/<station>/<year>")
# if not for the sub directory yearly it will class with the about bellow
def yearly(station, year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    # it is not parsed any more because we could not read it as a string
    df["    DATE"] = df["    DATE"].astype(str)
    # we could not read it as a string
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    # to make the end result more user friendly
    return result


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    # the name of the files is TG_STAID000001, TG_STAID000002 ... TG_STAID000100, that's why we use zfill(6) method
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    # the first 20 rows have general information and not real data, the name of the date column is "    DATE"
    temperature = df.loc[df["    DATE"] == date]['   TG'].squeeze()/10
    return {"station": station,
            "date": date,
            "temperature": temperature}


app.run(debug=True)
