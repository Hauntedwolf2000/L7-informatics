import sqlite3

#sqlite3 connection
conn = sqlite3.connect('myice_cream.db')
cursor = conn.cursor()

# creating the database
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Flavours (
        id INTEGER PRIMARY KEY,
        flavor_name TEXT NOT NULL,
        seasonal_availability TEXT
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS Inventory (
        id INTEGER PRIMARY KEY,
        flavor_id INTEGER,
        ingredient TEXT NOT NULL,
        quantity INTEGER,
        FOREIGN KEY (flavor_id) REFERENCES Flavours(id)
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS Allergens (
        id INTEGER PRIMARY KEY,
        ingredient TEXT NOT NULL,
        allergic_symptoms TEXT
    )
''')

#flavours table datas
flavour_data = [
    ('Vanilla', 'Year-round'),
    ('Chocolate', 'Year-round'),
    ('Strawberry', 'Spring-Summer'),
    ('Mint Chip', 'Year-round')
]

cursor.executemany('''
    INSERT INTO Flavours (flavor_name, seasonal_availability) VALUES (?, ?)
''', flavour_data)

#inventry table datas
inventory_data = [
    (1, 'Milk', 100),
    (1, 'Sugar', 50),
    (2, 'Cocoa', 80),
    (2, 'Milk', 120),
    (3, 'Strawberries', 60),
    (3, 'Milk', 100),
    (4, 'Mint Extract', 40),
    (4, 'Chocolate Chips', 70)
]

cursor.executemany('''
    INSERT INTO Inventory (flavor_id, ingredient, quantity) VALUES (?, ?, ?)
''', inventory_data)

#Allergens table dats
allergens_data = [
    ('Milk', 'Lactose intolerance, digestive issues'),
    ('Nuts', 'Anaphylaxis, hives'),
    ('Eggs', 'Allergic reactions, hives, swelling'),
    ('Soy', 'Allergic reactions, digestive issues')
]

cursor.executemany('''
    INSERT INTO Allergens (ingredient, allergic_symptoms) VALUES (?, ?)
''', allergens_data)

#save and close the connection to the database
conn.commit()
conn.close()
