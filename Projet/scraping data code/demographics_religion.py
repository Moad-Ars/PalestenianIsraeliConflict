from bs4 import BeautifulSoup
import requests
import pandas as pd
import re


url = "https://fr.wikipedia.org/wiki/D%C3%A9mographie_d%27Isra%C3%ABl"
response = requests.get(url)
year = []
juifs = []
musulmans = []
chretiens = []
druzes = []

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')
    for table in tables:
        caption = table.find('caption')
        if caption and "religion" in caption.text:
            for row in table.select('tr'):
                td_elements = row.find_all('td')
                if td_elements and "Total" not in td_elements[0].text.strip():
                    year.append(td_elements[0].text.strip())
                    # juifs.append((td_elements[1].text.replace(',', '.').strip('%')))
                    juifs.append(float((re.sub(r'[^0-9.,]', '', td_elements[1].text.strip())).replace(',', '.')))
                    musulmans.append(float((re.sub(r'[^0-9.,]', '', td_elements[2].text.strip())).replace(',', '.')))
                    chretiens.append(float((re.sub(r'[^0-9.,]', '', td_elements[3].text.strip())).replace(',', '.')))
                    druzes.append(float((re.sub(r'[^0-9.,]', '', td_elements[4].text.strip())).replace(',', '.')))
                    
print(year)
                    

df = pd.DataFrame({
    'Annee': year,
    'Juifs': juifs,
    'Musulmans': musulmans,
    'Chretiens': chretiens,
    'Druzes': druzes
})

# # Melt the DataFrame to reshape it
df_melted = pd.melt(df, id_vars=['Annee'], var_name='Religion', value_name='population totale')

# Display the resulting DataFrame
print(df_melted)
df_melted.to_csv('Immigration_With_Religion.csv', index=False) 