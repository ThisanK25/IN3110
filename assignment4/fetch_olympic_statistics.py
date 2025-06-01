"""
Task 4

collecting olympic statistics from wikipedia
"""

from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from requesting_urls import get_html

# Countries to submit statistics for
scandinavian_countries = ["Norway", "Sweden", "Denmark"]

# Summer sports to submit statistics for
summer_sports = ["Sailing", "Athletics", "Handball", "Football", "Cycling", "Archery"]


def report_scandi_stats(url: str, sports_list: list[str], work_dir: str | Path) -> None:
    """
    Given the url, extract and display following statistics for the Scandinavian countries:

      -  Total number of gold medals for for summer and winter Olympics
      -  Total number of gold, silver and bronze medals in the selected summer sports from sport_list
      -  The best country in number of gold medals in each of the selected summer sports from sport_list

    Display the first two as bar charts, and the last as an md. table and save in a separate directory.

    Parameters:
        url (str) : url to the 'All-time Olympic Games medal table' wiki page
        sports_list (list[str]) : list of summer Olympic games sports to display statistics for
        work_dir (str | Path) : (absolute) path to your current working directory

    Returns:
        None
    """

    # Make a call to get_scandi_stats
    # Plot the summer/winter gold medal stats
    # Iterate through each sport and make a call to get_sport_stats
    # Plot the sport specific stats
    # Make a call to find_best_country_in_sport for each sport
    # Create and save the md table of best in each sport stats

    work_dir = Path(work_dir)
    country_dict = get_scandi_stats(url)

    stats_dir = work_dir / "olympic_games_results"
    Path.mkdir(stats_dir, exist_ok=True)

    # plot total olympic medals
    plot_scandi_stats(country_dict, output_parent=stats_dir)

    best_in_sport = []
    sport_decisive = []
    # Valid values for medal ["Gold" | "Silver" |"Bronze"]
    medal = "Gold"

    for sport in sports_list:
        results: dict[str, dict[str, int]] = {
            "Norway": get_sport_stats(country_dict["Norway"]["url"], sport),
            "Sweden": get_sport_stats(country_dict["Sweden"]["url"], sport),
            "Denmark": get_sport_stats(country_dict["Denmark"]["url"], sport)
        }

        # plot medals given sport
        plot_sport_stats(results, sport, output_parent=stats_dir)

        # find sports with one best country and add both sport and country to lists
        best = find_best_country_in_sport(results, medal=medal)
        if best != "None" and not best.__contains__("/"):
            best_in_sport.append(best)
            sport_decisive.append(sport)

    # create .md table of best countries in sport
    best_table = {"Sport": pd.Series(sport_decisive), "Best country": pd.Series(best_in_sport)}
    table = pd.DataFrame.to_markdown(best_table, index=False)

    # write table to file
    with open(stats_dir/f"best_of_sport_by_{medal}.md", "w", encoding='utf8') as f:
        print(f"Creating best_of_sport_by_{medal}.md")
        f.write(table)
    f.close()


def get_scandi_stats(
    url: str,
) -> dict[str, dict[str, str | dict[str, int]]]:
    """Given the url, extract the urls for the Scandinavian countries,
       as well as number of gold medals acquired in summer and winter Olympic games
       from 'List of NOCs with medals' table.

    Parameters:
      url (str): url to the 'All-time Olympic Games medal table' wiki page

    Returns:
      country_dict: dictionary of the form:
        {
            "country": {
                "url": "https://...",
                "medals": {
                    "Summer": 0,
                    "Winter": 0,
                },
            },
        }

        with the tree keys "Norway", "Denmark", "Sweden".
    """

    # Extract and parse html
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    # 'List of NOC's with medals' is the second table in the article 
    table = soup.find("table").find_next("table")
    base_url = "https://en.wikipedia.org"

    # extract all rows in table
    rows = table.find_all("tr")

    # create dictionary
    country_dict: dict[str, dict[str, str | dict[str, int]]] = {}

    for row in rows:
        # extract all columns in row
        cols = row.find_all("td")
        if cols:
            # only one occurrence of '<a>' in column
            name = cols[0].find('a').get_text()
            # if country is scandinavian
            if name in scandinavian_countries:
                country_dict[name] = {"url": f"{base_url}/wiki/{name}_at_the_Olympics", "medals": {"Summer": 0, "Winter": 0}}
                # Summer gold medals in third column
                country_dict[name]["medals"]["Summer"] = int(cols[2].get_text())
                # Winter gold medals in eighth column
                country_dict[name]["medals"]["Winter"] = int(cols[7].get_text())

    return country_dict


def get_sport_stats(country_url: str, sport: str) -> dict[str, int]:
    """Given the url to country specific performance page, get the number of gold, silver, and bronze medals
      the given country has acquired in the requested sport in summer Olympic games.

    Parameters:
        - country_url (str) : url to the country specific Olympic performance wiki page
        - sport (str) : name of the summer Olympic sport in interest. Should be used to filter rows in the table.

    Returns:
        - medals (dict[str, int]) : dictionary of number of medal acquired in the given sport by the country
                          Format:
                          {"Gold" : x, "Silver" : y, "Bronze" : z}
    """
    
    # extract and parse html
    html = get_html(country_url)
    soup = BeautifulSoup(html, "html.parser")
    # First table with class 'jquery_tablesorter'
    table = soup.find("table", class_="wikitable sortable plainrowheaders jquery-tablesorter")

    medals = {
        "Gold": 0,
        "Silver": 0,
        "Bronze": 0,
    }

    # extract all rows in table
    rows = table.find_all("tr")

    for row in rows:
        # only one occurrence of '<a>' in cell        
        sport_cell = row.find("a")
        # extract all columns in row
        medal_cols = row.find_all("td")
        if sport_cell and medal_cols:
            # set amount of medals given sport
            if sport_cell.get_text() == sport:
                medals["Gold"] = int(medal_cols[0].get_text())
                medals["Silver"] = int(medal_cols[1].get_text())
                medals["Bronze"] = int(medal_cols[2].get_text())
    return medals


def find_best_country_in_sport(
    results: dict[str, dict[str, int]], medal: str = "Gold"
) -> str:
    """Given a dictionary with medal stats in a given sport for the Scandinavian countries, return the country
        that has received the most of the given `medal`.

    Parameters:
        - results (dict) : a dictionary of country specific medal results in a given sport. The format is:
                        {"Norway" : {"Gold" : 1, "Silver" : 2, "Bronze" : 3},
                         "Sweden" : {"Gold" : 1, ....},
                         "Denmark" : ...
                        }
        - medal (str) : medal type to compare for. Valid parameters: ["Gold" | "Silver" |"Bronze"]. Should be used as a key
                          to the medal dictionary.
    Returns:
        - best (str) : name of the country(ies) leading in number of gold medals in the given sport
                       If one country leads only, return its name, like for instance 'Norway'
                       If two countries lead return their names separated with '/' like 'Norway/Sweden'
                       If all or none of the countries lead, return string 'None'
    """
    
    valid_medals = {"Gold", "Silver", "Bronze"}
    if medal not in valid_medals:
        raise ValueError(
            f"{medal} is invalid parameter for ranking, must be in {valid_medals}"
        )

    # Get the requested medals and determine the best
    best = "None"
    val = 0
    for country, amount in results.items():
        if amount[medal] == val:
            if best != "None":
                # add country if tie
                best += "/" + country
            else:
                best = country
        elif amount[medal] > val:
            best = country
            # update val
            val = amount[medal]
    
    # If all countries tie, set back to 'None'
    if len(best.split("/")) == len(scandinavian_countries):
        best = "None"

    return best


# Define your own plotting functions and optional helper functions


def plot_scandi_stats(
    country_dict: dict[str, dict[str, str | dict[str, int]]],
    output_parent: str | Path | None = None,
) -> None:
    """Plot the number of gold medals in summer and winter games for each of the scandi countries as bars.

    Parameters:
        - country_dict (dict[str, dict[str, int]]) : a nested dictionary of country names and the corresponding number of summer and winter
                            gold medals from 'List of NOCs with medals' table.
                            Format:
                            {"country_name": {"Summer" : x, "Winter" : y}}
        - output_parent (str | Path) : parent file path to save the plot in
    Returns:
        - None
    """

    width = 0.25

    # to center labels
    bar1 = np.arange(len(scandinavian_countries)) - width/2
    bar2 = bar1 + width

    summer_medals = []
    winter_medals = []
    # add number of medals per season to separate lists
    for country in scandinavian_countries:
        summer_medals.append(country_dict[country]["medals"]["Summer"])
        winter_medals.append(country_dict[country]["medals"]["Winter"])

    # plotting the seasonal medals of each country
    b1 = plt.bar(bar1, summer_medals, color='r', width=width)
    plt.bar_label(b1)
    b2 = plt.bar(bar2, winter_medals, color='b', width=width)
    plt.bar_label(b2)

    # axis names
    plt.xlabel("Countries")
    plt.ylabel("Number of gold medals")
    # use the names as the labels for the bars
    plt.xticks(range(len(scandinavian_countries)), scandinavian_countries)
    # add the legend with the colors for each season
    plt.legend(["Summer", "Winter"])
    # turn off gridlines
    plt.grid(False)
    # set the title
    plt.title("Olympic gold medals for Scandinavia by season")
    # save the figure to a file
    filename = output_parent/"total_medal_ranking.png"
    print(f"Creating {filename.name}")
    plt.savefig(filename)
    plt.close()


def plot_sport_stats(
    results: dict[str, dict[str, int]],
    sport: str,
    output_parent: str | Path | None = None
) -> None:
    """Plot the number of gold, silver and bronze medals in a given sport for each of the scandi countries as bars.

    Parameters:
        - results (dict) : a dictionary of country specific medal results in a given sport. The format is:
                        {"Norway" : {"Gold" : 1, "Silver" : 2, "Bronze" : 3},
                         "Sweden" : {"Gold" : 1, ....},
                         "Denmark" : ...
                        }
        - sport (str) : the sport to plot for
        - output_parent (str | Path) : parent file path to save the plot in
    Returns:
        - None
    """

    width = 0.25

    # to center labels
    bar1 = np.arange(len(scandinavian_countries)) - width
    bar2 = bar1 + width
    bar3 = bar2 + width

    gold_medals = []
    silver_medals = []
    bronze_medals = []
    # categorize and add number of medals to separate lists
    for country in scandinavian_countries:
        gold_medals.append(results[country]["Gold"])
        silver_medals.append(results[country]["Silver"])
        bronze_medals.append(results[country]["Bronze"])

    # plotting the medals of each country in sport
    b1 = plt.bar(bar1, gold_medals, color='gold', width=width)
    plt.bar_label(b1)
    b2 = plt.bar(bar2, silver_medals, color='silver', width=width)
    plt.bar_label(b2)
    b3 = plt.bar(bar3, bronze_medals, color="#cd7f32", width=width)
    plt.bar_label(b3)

    # axis names
    plt.xlabel("Countries")
    plt.ylabel("Number of medals")
    # use the names as the labels for the bars
    plt.xticks(range(len(scandinavian_countries)), scandinavian_countries)
    # add the legend with each type of medal
    plt.legend(["Gold", "Silver", "Bronze"])
    # turn off gridlines
    plt.grid(False)
    # set the title
    plt.title(f"Olympic medals in {sport} for Scandinavia")
    # save the figure to a file
    filename = output_parent/f"{sport}_medal_ranking.png"
    print(f"Creating {filename.name}")
    plt.savefig(filename)
    plt.close()


# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table"
    work_dir = Path.cwd()
    report_scandi_stats(url, summer_sports, work_dir)