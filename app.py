from flask import Flask, render_template, request, redirect, url_for,jsonify
import sqlite3

app = Flask(__name__)

# Database configuration
DATABASE = 'myice_cream.db'

# Function to establish database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

#index page with login form
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # default username and password
    if username == 'user' and password == '1234':
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('customer'))

#admin page
@app.route('/admin')
def admin():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Flavours')
    flavours = cursor.fetchall()
    cursor.execute('SELECT * FROM Inventory')
    inventory = cursor.fetchall()
    cursor.execute('SELECT * FROM Allergens')
    allergens = cursor.fetchall()
    cursor.execute('SELECT * FROM Customer_sugested_flavour')
    Customer_sugested_flavour = cursor.fetchall()

    conn.close()

    return render_template('admin.html', flavours=flavours, inventory=inventory, allergens=allergens ,Customer_sugested_flavour=Customer_sugested_flavour )

# deletion of a flavour,inventry,allergen
@app.route('/delete_flavour/<int:id>', methods=['POST'])
def delete_flavour(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Flavours WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))
@app.route('/delete_inventory/<int:id>', methods=['POST'])
def delete_inventory(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Inventory WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/delete_allergen/<int:id>', methods=['POST'])
def delete_allergen(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Allergens WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/delete_Sflavour/<int:id>', methods=['POST'])
def delete_Sflavour(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Customer_sugested_flavour WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

#iventry managment
@app.route('/increase_quantity/<int:id>', methods=['POST'])
def increase_quantity(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE Inventory SET quantity = quantity + 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))
@app.route('/decrease_quantity/<int:id>', methods=['POST'])
def decrease_quantity(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE Inventory SET quantity = quantity - 1 WHERE id = ? AND quantity > 0', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

#customer page
@app.route('/customer')
def customer():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Flavours')
    flavours = cursor.fetchall()

    cursor.execute('SELECT * FROM Inventory')
    inventory = cursor.fetchall()
    conn.close()
    return render_template('customer.html', flavours=flavours,inventory=inventory)





@app.route('/search', methods=['GET', 'POST'])
def search():
    conn = get_db_connection()
    flavours = []
    inventory = {}

    if request.method == 'POST':
        search_term = request.form['search']
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Flavours WHERE flavor_name LIKE ?', ('%' + search_term + '%',))
        flavours = cursor.fetchall()
        for flavour in flavours:
            cursor.execute('SELECT * FROM Inventory WHERE flavor_id = ?', (flavour['id'],))
            inventory[flavour['id']] = cursor.fetchall()

        conn.close()

        return render_template('search.html', flavours=flavours, inventory=inventory, search_term=search_term)
    conn.close()

    return render_template('search.html', flavours=flavours, inventory=inventory, search_term='')

#suggestion page
@app.route('/suggest-flavour', methods=['GET', 'POST'])
def suggest_flavour():
    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'flavour':
            flavor_name = request.form['flavor_name']
            ingredient = request.form['ingredient']
            seasonal_availability = request.form['seasonal_availability']

            conn = get_db_connection()
            conn.execute('''
                INSERT INTO Customer_sugested_flavour (flavor_name, ingredient, seasonal_availability)
                VALUES (?, ?, ?)
            ''', (flavor_name, ingredient, seasonal_availability))
            conn.commit()
            conn.close()
            return jsonify({"success": "flavour"})

        elif form_type == 'allergen':
            ingredient = request.form['allergen_ingredient']
            allergic_symptoms = request.form['allergic_symptoms']

            conn = get_db_connection()
            conn.execute('''
                INSERT INTO Allergens (ingredient, allergic_symptoms)
                VALUES (?, ?)
            ''', (ingredient, allergic_symptoms))
            conn.commit()
            conn.close()
            return jsonify({"success": "allergen"})

    return render_template('suggest_flavour.html')


if __name__ == '__main__':
    app.run(debug=True)
