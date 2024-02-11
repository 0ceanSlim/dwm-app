import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.woodus.com/den/games/dwm2gbc/skills.php"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    skill_tables = soup.find_all('table', {'border': '0', 'width': '95%', 'cellspacing': '0', 'cellpadding': '4', 'align': 'center'})

    with open('skills_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Skill Name', 'MP', 'Minimum Level', 'Minimum HP', 'Minimum Attack', 'Minimum Defense', 'Minimum Agility', 'Minimum Intelligence', 'Natural', 'Combine', 'Upgrades', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for table in skill_tables:
            skill_name = table.find('thead').find('th').text.strip()

            # Extract the stats directly from the table rows
            rows = table.find_all('tr')[1:]  # Skip the header row
            skill_stats = {'Skill Name': skill_name}

            for row in rows:
                columns = row.find_all(['td', 'th'])
                stat_name = columns[0].text.strip().rstrip(':')

                # Check if the stat is 'Natural', 'Combine', or 'Upgrades'
                if stat_name in ['Natural', 'Combine', 'Upgrades']:
                    stat_value = ', '.join([item.strip() for item in columns[1].stripped_strings])
                else:
                    stat_value = columns[1].text.strip()

                skill_stats[stat_name] = stat_value

            # Check if there's at least one stat other than 'Skill Name' and 'Description'
            if len(skill_stats) > 2:
                writer.writerow(skill_stats)

    print("CSV file 'skills_data.csv' created successfully.")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
