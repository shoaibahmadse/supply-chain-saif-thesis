# app.py

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np

model = joblib.load('random_forest_model.pkl')

label_encoder = LabelEncoder()
scaler = StandardScaler()

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('supply_chain.db')
    conn.row_factory = sqlite3.Row  # This allows us to access the columns by name
    return conn

@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM product').fetchall()
    conn.close()

    # Convert the row objects to dictionaries
    products_list = [dict(row) for row in products]
    # Convert products_list to DataFrame
    df = pd.DataFrame(products_list)

    # Apply label encoding to categorical columns
    df['Customer_ID'] = label_encoder.fit_transform(df['Customer_ID'])
    df['Market'] = label_encoder.fit_transform(df['Market'])
    df['product_name'] = label_encoder.fit_transform(df['product_name'])
    df['Order_Priority'] = label_encoder.fit_transform(df['Order_Priority'])

    # Fit and transform the numerical columns
    numerical_cols = ['quantity', 'discount', 'Shipping_Cost']
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

    df = df.rename(columns={'Customer_ID': 'Customer ID'})
    df = df.rename(columns={'discount': 'Discount'})
    df = df.rename(columns={'Order_Priority': 'Order Priority'})
    df = df.rename(columns={'product_name': 'Product Name'})
    df = df.rename(columns={'quantity': 'Quantity'})
    df = df.rename(columns={'Shipping_Cost': 'Shipping Cost'})
    df = df.drop(columns=['sales'])

    # Prepare the features for prediction
    X = df

    # Make predictions
    predictions = model.predict(X)

    # Add predictions to the products_list
    for i, product in enumerate(products_list):
        product['Predicted_Sales'] = predictions[i]

    # Now products_list contains the predictions
    print(products_list)

    return jsonify(products_list)


@app.route('/products', methods=['POST'])
def update_product():
    data = request.json
    Customer_ID = data['Customer_ID']
    updates = data['updates']
    conn = get_db_connection()
    c = conn.cursor()
    for key, value in updates.items():
        c.execute(f'UPDATE product SET {key} = ? WHERE Customer_ID = ?', (value, Customer_ID))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True)
