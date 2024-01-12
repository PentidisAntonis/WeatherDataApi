from flask import Flask, render_template
import pandas as pd


app = Flask("Website")


@app.route("/")
def home():
    return render_template("home.html")


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
