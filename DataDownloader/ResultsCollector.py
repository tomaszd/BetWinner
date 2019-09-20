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
            )
            self.teams.append(single_team_dict)

    def getTeams(self):
        return self.teams


if __name__ == "__main__":
    resultsCollector = ResultsCollector("http://www.90minut.pl/liga/1/liga10874.html")
    resultsCollector.download_data()
    bs_data = resultsCollector.get_data()
    parser = ResultsParser(bs_data)
    parser.parseData()
    print("Sytuacja w tabeli: ")
    for i, team in enumerate(parser.teams):
        print(i + 1, " ", team)
