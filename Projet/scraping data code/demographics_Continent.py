from bs4 import BeautifulSoup
import requests
import pandas as pd


url = "https://fr.wikipedia.org/wiki/D%C3%A9mographie_d%27Isra%C3%ABl"
response = requests.get(url)
demographie = []
periode_immigration = []
amerique = []
europe = []
afrique = []
asie = []
total = []

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')
    for table in tables:
        caption = table.find('caption')
        if caption and "Immigration" in caption.text:
            for row in table.select('tr'):
                td_elements = row.find_all('td')
                if td_elements and "Total" not in td_elements[0].text.strip():
                    periode_immigration.append(td_elements[0].text.strip())
                    amerique.append(td_elements[1].text.strip(r"\xa "))
                    europe.append(td_elements[2].text.strip(r"\xa "))
                    afrique.append(td_elements[3].text.strip(r"\xa "))
                    asie.append(td_elements[4].text.strip(r"\xa "))
                    total.append(td_elements[5].text.strip(r"\xa "))
                    

df = pd.DataFrame({
    'Période d’immigration': periode_immigration,
    'Amerique': amerique,
    'Europe': europe,
    'Afrique': afrique,
    'Asie': asie
})

# Melt the DataFrame to reshape it
df_melted = pd.melt(df, id_vars=['Période d’immigration'], var_name='Continent', value_name='numberOfImmigration')

# Display the resulting DataFrame
print(df_melted)
df_melted.to_csv('../Immigration_With_Continent.csv', index=False) 