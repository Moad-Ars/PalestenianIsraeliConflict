from bs4 import BeautifulSoup
import requests
import pandas as pd


url = "https://en.wikipedia.org/wiki/List_of_Israeli_settlements#cite_note-Israelpopulations-7%23cite_note-Israelpopulations-7"
response = requests.get(url)
colonies = []

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.select('table:nth-of-type(2)')
    for row in table[-1].find_all('tr'):
        td_elements = row.find_all('td')
        if td_elements:
            Name = td_elements[0].get_text(strip=True)
            Hebrew = td_elements[1].get_text(strip=True)
            Population = td_elements[2].get_text(strip=True)
            Establishment = td_elements[3].get_text(strip=True)
            Council = td_elements[4].get_text(strip=True)
            colonies.append([Name, Hebrew, Population, Establishment, Council])

df = pd.DataFrame(colonies, columns=['Name', 'Hebrew', 'Population', 'Establishment', 'Council'])

df.to_csv('coloniesScripted.csv', index=True)           

