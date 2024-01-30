import sqlite3
import xml.etree.ElementTree as ET

def create_tables(conn):
    cursor = conn.cursor()

    # Families table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS families (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    ''')

    # Monsters table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monsters (
            id INTEGER PRIMARY KEY,
            family_id INTEGER,
            name TEXT,
            in_story BOOLEAN,
            agl INTEGER,
            int INTEGER,
            maxlvl INTEGER,
            atk INTEGER,
            mp INTEGER,
            exp INTEGER,
            hp INTEGER,
            def INTEGER,
            FOREIGN KEY (family_id) REFERENCES families (id)
        );
    ''')

    # Spawn Locations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spawn_locations (
            id INTEGER PRIMARY KEY,
            monster_id INTEGER,
            map TEXT,
            description TEXT,
            FOREIGN KEY (monster_id) REFERENCES monsters (id)
        );
    ''')

    # Skills table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY,
            monster_id INTEGER,
            skill TEXT,
            FOREIGN KEY (monster_id) REFERENCES monsters (id)
        );
    ''')

    # Breeds table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS breeds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT
        )
    ''')

    # Breed Requirements table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS breed_requirements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            breed_id INTEGER,
            family TEXT,
            monster TEXT,
            FOREIGN KEY (breed_id) REFERENCES breeds(id)
        )
    ''')

    # Skills Data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    ''')

    # Skill Requirements table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skill_requirements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_data_id INTEGER,
            lvl INTEGER,
            hp INTEGER,
            mp INTEGER,
            atk INTEGER,
            def INTEGER,
            agl INTEGER,
            int INTEGER,
            FOREIGN KEY (skill_data_id) REFERENCES skills_data(id)
        )
    ''')

    # Combine From table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS combine_from (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_data_id INTEGER,
            skill TEXT,
            FOREIGN KEY (skill_data_id) REFERENCES skills_data(id)
        )
    ''')

    # Precursor table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS precursor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_data_id INTEGER,
            precursor TEXT,
            FOREIGN KEY (skill_data_id) REFERENCES skills_data(id)
        )
    ''')

    conn.commit()

def insert_data(xml_file, database_file):
    # Parse XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)

    # Create tables if they don't exist
    create_tables(conn)

    cursor = conn.cursor()

    for family_elem in root.findall('./families/family'):
        family_name = family_elem.attrib['name']
        cursor.execute('INSERT INTO families (name) VALUES (?)', (family_name,))
        family_id = cursor.lastrowid

        for monster_elem in family_elem.findall('./monsters/monster'):
            monster_name = monster_elem.attrib['name']
            in_story = monster_elem.attrib.get('in_story', False)

            # Insert into monsters table
            cursor.execute('''
                INSERT INTO monsters (family_id, name, in_story, agl, int, maxlvl, atk, mp, exp, hp, def)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                family_id,
                monster_name,
                in_story,
                int(monster_elem.find('growth').attrib.get('agl', 0)),
                int(monster_elem.find('growth').attrib.get('int', 0)),
                int(monster_elem.find('growth').attrib.get('maxlvl', 0)),
                int(monster_elem.find('growth').attrib.get('atk', 0)),
                int(monster_elem.find('growth').attrib.get('mp', 0)),
                int(monster_elem.find('growth').attrib.get('exp', 0)),
                int(monster_elem.find('growth').attrib.get('hp', 0)),
                int(monster_elem.find('growth').attrib.get('def', 0))
            ))

            monster_id = cursor.lastrowid

            # Insert into skills table
            for skill_elem in monster_elem.findall('skills/skill'):
                cursor.execute('INSERT INTO skills (monster_id, skill) VALUES (?, ?)', (monster_id, skill_elem.text))

            # Insert into spawn_locations table
            for location_elem in monster_elem.findall('spawn-locations/location'):
                cursor.execute('INSERT INTO spawn_locations (monster_id, map, description) VALUES (?, ?, ?)',
                               (monster_id, location_elem.find('map').text, location_elem.find('description').text))

            
    for breed_elem in root.findall('.//breed'):
        target = breed_elem.attrib.get('target')
        cursor.execute('INSERT INTO breeds (target) VALUES (?)', (target,))
        breed_id = cursor.lastrowid

        for base_elem in breed_elem.findall('.//breed-requirement[@family]'):
            family_name = base_elem.attrib.get('family')
            cursor.execute('INSERT INTO breed_requirements (breed_id, family) VALUES (?, ?)', (breed_id, family_name))

        for mate_elem in breed_elem.findall('.//breed-requirement[@monster]'):
            monster_name = mate_elem.attrib.get('monster')
            cursor.execute('INSERT INTO breed_requirements (breed_id, monster) VALUES (?, ?)', (breed_id, monster_name))

    for skill_data_elem in root.findall('.//skill-data'):
        skill_name = skill_data_elem.attrib.get('name')
        cursor.execute('INSERT INTO skills_data (name) VALUES (?)', (skill_name,))
        skill_data_id = cursor.lastrowid

        requirements_elem = skill_data_elem.find('.//skill-requirements')
        lvl = int(requirements_elem.attrib.get('lvl', 0))
        hp = int(requirements_elem.attrib.get('hp', 0))
        mp = int(requirements_elem.attrib.get('mp', 0))
        atk = int(requirements_elem.attrib.get('atk', 0))
        def_ = int(requirements_elem.attrib.get('def', 0))
        agl = int(requirements_elem.attrib.get('agl', 0))
        int_ = int(requirements_elem.attrib.get('int', 0))

        cursor.execute('INSERT INTO skill_requirements (skill_data_id, lvl, hp, mp, atk, def, agl, int) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                       (skill_data_id, lvl, hp, mp, atk, def_, agl, int_))

        combine_from_elem = skill_data_elem.find('.//combine-from')
        if combine_from_elem is not None:
            for combine_skill_elem in combine_from_elem.findall('.//skill'):
                combine_skill_name = combine_skill_elem.text
                cursor.execute('INSERT INTO combine_from (skill_data_id, skill) VALUES (?, ?)', (skill_data_id, combine_skill_name))

        precursor_elem = skill_data_elem.find('.//precursor')
        if precursor_elem is not None:
            precursor_name = precursor_elem.text
            cursor.execute('INSERT INTO precursor (skill_data_id, precursor) VALUES (?, ?)', (skill_data_id, precursor_name))

    # Commit changes and close the connection
    conn.commit()
    conn.close()


# Example usage
insert_data('data.xml', 'monsters.db')
