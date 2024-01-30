import xml.etree.ElementTree as ET
import sqlite3

DATABASE = "monsters.db"


def connect_db():
    return sqlite3.connect(DATABASE)


def create_tables():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS breeds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL
            );
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS breed_requirements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                breed_id INTEGER NOT NULL,
                requirement_type TEXT NOT NULL,
                requirement_value TEXT NOT NULL,
                FOREIGN KEY (breed_id) REFERENCES breeds (id)
            );
        """
        )
        conn.commit()


def insert_breeding_data(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    with connect_db() as conn:
        cursor = conn.cursor()

        for breed_element in root.findall(".//breeds/breed"):
            target = breed_element.get("target")

            cursor.execute("INSERT INTO breeds (target) VALUES (?)", (target,))
            breed_id = cursor.lastrowid

            base_requirements = breed_element.find("./base")
            insert_breed_requirements(cursor, breed_id, base_requirements, "base")

            mate_requirements = breed_element.find("./mate")
            insert_breed_requirements(cursor, breed_id, mate_requirements, "mate")

        conn.commit()


def insert_breed_requirements(cursor, breed_id, requirements_element, requirement_type):
    for requirement_element in requirements_element.findall("./breed-requirement"):
        family = requirement_element.get("family")
        monster = requirement_element.get("monster")

        cursor.execute(
            """
            INSERT INTO breed_requirements (breed_id, requirement_type, requirement_value)
            VALUES (?, ?, ?)
        """,
            (breed_id, requirement_type, family or monster),
        )


if __name__ == "__main__":
    create_tables()
    insert_breeding_data("data.xml")
    print("Breeding data inserted successfully.")
