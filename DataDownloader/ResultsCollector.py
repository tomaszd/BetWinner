import json

import os
import requests
from bs4 import BeautifulSoup


class ResultsCollector():
    def __init__(self, URL=None):
        print("Data downloading started...")
        if URL is None:
            self.result_URL = None
        else:
            self.setURL(URL)

        self.data = None

    def setURL(self, URL):
        print("Setting URL:  " + URL)
        self.result_URL = URL

    def download_data(self):
        data = requests.get(self.result_URL)
        self.data = BeautifulSoup(data.text, features="lxml")

    def get_data(self):
        if self.data is None:
            print("WARNING there is no data yet ")
        return self.data


class ResultsParser():
    def __init__(self, bs_data):
        self.raw_data = bs_data
        self.teams = []
        self.results = []

    def parseData(self):
        all_data = self.raw_data.find_all("a", {"class": "main"})
        only_teams = [x for x in all_data if "skarb" in x["href"]]

        for team in only_teams:
            single_team_data = team.parent.parent.find_all("td")
            single_team_dict = dict(
                place_in_table=single_team_data[0].text,
                name=single_team_data[1].text.strip(),
                matches=single_team_data[2].text,
                points=single_team_data[3].text,
                win=single_team_data[4].text,
                loose=single_team_data[5].text,
                goals=single_team_data[6].text,
                last_matches=[]
            )
            self.teams.append(single_team_dict)

        only_teams_names = [x["name"] for x in self.teams]
        all_team_results = self.raw_data.find_all("table", {"class": "main2"})[1].find_all("tr")
        for i, single_team_results in enumerate(all_team_results[1:]):
            team_result_dict = {}
            for j, single_result in enumerate(single_team_results.find_all("td")[2:]):
                if single_result.text == '    ':
                    team_result_dict[only_teams_names[j]] = "N/A"
                else:
                    team_result_dict[only_teams_names[j]] = single_result.text.strip()
            pass
            self.teams[i]["results"] = team_result_dict
        series = []

        for single_serie in self.raw_data.find_all("table", {"class": "main", "align": "center"}):
            serie = []
            if "Kolejka" in single_serie.text:
                continue

            for single_match in single_serie.find_all("tr"):
                rows = single_match.find_all("td")
                if len(rows) != 4:
                    continue
                home_team, result, away_team, date = [x.text.strip() for x in rows]
                match = {"home": home_team,
                         "away": away_team,
                         "result": result,
                         "date": date}

                self.add_last_result(match)

                serie.append(match)
            if result == "-":
                break
            series.append(serie)

    def getTeams(self):
        return self.teams

    def add_last_result(self, match):
        for team in self.teams:
            if team["name"] in [match["home"], match["away"]]:
                team["last_matches"].append(match)
    def save_dat_into_json(self):
        with open(os.path.join("data",'data.txt'), 'w') as outfile:
            json.dump(self.teams, outfile)



if __name__ == "__main__":
    resultsCollector = ResultsCollector("http://www.90minut.pl/liga/1/liga10874.html")
    resultsCollector.download_data()
    bs_data = resultsCollector.get_data()
    parser = ResultsParser(bs_data)
    parser.parseData()
    print("Sytuacja w tabeli: ")
    for i, team in enumerate(parser.teams):
        print(i + 1, " ", team)
    parser.save_dat_into_json()
