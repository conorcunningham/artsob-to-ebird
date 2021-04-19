from bs4 import BeautifulSoup
import json

line_start = "<tr class='highlight1"
bird_names = {}

with open("../data/avibase-raw-european-bird-names", "r") as file:
    for line in file:
        if line.startswith(line_start):
            try:
                soup = BeautifulSoup(line)
                common= soup.findAll("td")[0].renderContents().decode("utf-8")
                scientific = soup.findAll("i")[0].renderContents().decode("utf-8")
                bird_names[scientific] = common
            except IndexError:
                continue

with open('result.json', 'w') as fp:
    json.dump(bird_names, fp)
