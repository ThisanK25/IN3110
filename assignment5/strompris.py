"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""

import datetime
import warnings

import altair as alt
import pandas as pd
import requests
import requests_cache

# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()

# suppress a warning with altair 4 and latest pandas
warnings.filterwarnings("ignore", ".*convert_dtype.*", FutureWarning)


# task 5.1:


def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API

    Arguments:
    - date (datetime.date): The date to fetch data for. Default is None.
    - location (str): The location code to fetch data for. Default is "NO1".
    
    Returns:
    - df (pd.DataFrame): Data frame of energy prices in a day.
    """
    # set today's date as default date
    if date is None:
        date = datetime.date.today()

    # prepend 0 to day and month if any are single digit
    month = str(date.month).zfill(2)
    day = str(date.day).zfill(2)

    # request url data
    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{date.year}/{month}-{day}_{location}.json"
    response = requests.get(url)

    nok_per_kwh = []
    time_start = []
    # iterate through the json, add price and start time to lists
    for r in response.json():
        nok_per_kwh.append(r["NOK_per_kWh"])
        time_start.append(r["time_start"])

    # create data frame from lists
    df = pd.DataFrame({
        "NOK_per_kWh": nok_per_kwh,
        "time_start": time_start
    })

    # Change time zone in case of crossing daylight savings time
    df["time_start"] = pd.to_datetime(df["time_start"], utc=True).dt.tz_convert("Europe/Oslo")

    return df


# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "NO1": "Oslo",
    "NO2": "Kristiansand",
    "NO3": "Trondheim",
    "NO4": "Tromsø",
    "NO5": "Bergen"
}

# task 1:


def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations: list[str] = tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame

    Arguments:
    - end_date (datetime.date): The final day to fetch data for. Default is None.
    - days (int): Amount of days up to end_days to check data for. Default is 7.
    - locations (list[str]): A list of location codes to fetch data for. Default is tuple(LOCATION_CODES.keys()).

    Returns:
    - df (pd.DataFrame): Data frame of energy prices in a time period.
    """

    # set today's date as default date
    if end_date is None:
        end_date = datetime.date.today()

    # Initialize data frame
    df = pd.DataFrame()

    for i in reversed(range(days)):
        # Fetch data starting with first date in range
        current_date = end_date - datetime.timedelta(i)
        for location in locations:
            # Fetch data for each location
            df_day_loc = fetch_day_prices(current_date, location)
            # Add columns for locations and codes
            df_day_loc["location_code"] = location
            df_day_loc["location"] = LOCATION_CODES[location]
            # Expand data frame with data for each date and location
            df = pd.concat([df, df_day_loc])

    return df

# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot energy prices over time

    x-axis should be time_start
    y-axis should be price in NOK
    each location should get its own line

    Arguments:
    - df (pd.DataFrame): Data frame of energy prices in a time period.

    Returns:
    - chart (alt.Chart): Chart of data provided by df.
    """
    
    # set x- and y-values and legend to line chart
    chart = alt.Chart(df).mark_line().encode(
        x = "time_start:T",
        y = "NOK_per_kWh:Q",
        color = "location:N"
    )

    return chart


# Task 5.4


def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    x-axis should be time_start (day resolution)
    y-axis should be price in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """
    ...


# Task 5.6

ACTIVITIES = {
    # activity name: energy cost in kW
    ...
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.

    Make sure to document arguments and return value...
    """
    raise NotImplementedError("Remove me when you implemnt this optional task")

    ...


def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()
