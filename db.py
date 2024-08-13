# create_database.py

import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('supply_chain.db')
c = conn.cursor()

# Create the product table
c.execute('''
CREATE TABLE IF NOT EXISTS product (
    Customer_ID TEXT NOT NULL, 
    Market TEXT NOT NULL,
    product_name TEXT NOT NULL,
    sales REAL NOT NULL,
    quantity INTEGER NOT NULL,
    discount REAL NOT NULL,
    Shipping_Cost REAL NOT NULL,
    Order_Priority TEXT NOT NULL
)
''')

# Insert sample data into the product table
c.execute('''
INSERT INTO product (Customer_ID, Market, product_name, sales, quantity, discount, Shipping_Cost, Order_Priority) VALUES
("HM-14860", "US", "OIC Stacking Trays", 10.02, 3, 0.0, 0.78, "Medium"),
("TS-21610", "LATAM", "Motorola Audio Dock, Cordless", 469.92, 5, 0.2, 23.31, "High"),
("ML-17395", "EU", "BIC Markers, Water Color", 118.440, 4, 0.0, 10.70, "High"),
("JR-5670", "EMEA", "Enermax Message Books, Recycled", 22.410, 1, 0.0, 1.82, "Medium"),
("AF-10870", "LATAM", "Cisco Office Telephone, VoIP", 429.600, 8, 0.0, 72.19, "Low")
''')
# print(c.execute('SELECT * FROM product').fetchall())

# Commit the changes and close the connection
conn.commit()
conn.close()

"""("HM-14860", "US", "OIC Stacking Trays", 10.02, 3, 0.0, 0.78, "Medium")
("TS-21610", "LATAM", "Motorola Audio Dock, Cordless", 469.92, 5, 0.2, 23.31, "High")
("ML-17395", "EU", "BIC Markers, Water Color", 118.440, 4, 0.0, 10.70, "High")
("JR-5670", "EMEA", "Enermax Message Books, Recycled", 22.410, 1, 0.0, 1.82, "Medium")
("AF-10870", "LATAM", "Cisco Office Telephone, VoIP", 429.600, 8, 0.0, 72.19, "Low")"""