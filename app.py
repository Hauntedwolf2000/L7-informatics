from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database configuration
DATABASE = 'myice_cream.db'

# Function to establish database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Route to display index page with login form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if username and password are correct
    if username == 'user' and password == '1234':
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('customer'))

# Route to display admin page with all data from database
@app.route('/admin')
def admin():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch data from Flavours table
    cursor.execute('SELECT * FROM Flavours')
    flavours = cursor.fetchall()

    # Fetch data from Inventory table
    cursor.execute('SELECT * FROM Inventory')
    inventory = cursor.fetchall()

    # Fetch data from Allergens table
    cursor.execute('SELECT * FROM Allergens')
    allergens = cursor.fetchall()

    conn.close()

    return render_template('admin.html', flavours=flavours, inventory=inventory, allergens=allergens)

# Route to handle deletion of a flavour
@app.route('/delete_flavour/<int:id>', methods=['POST'])
def delete_flavour(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Flavours WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

# Route to handle deletion of an inventory item
@app.route('/delete_inventory/<int:id>', methods=['POST'])
def delete_inventory(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Inventory WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))



# Route to handle increasing the quantity of an inventory item
@app.route('/increase_quantity/<int:id>', methods=['POST'])
def increase_quantity(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE Inventory SET quantity = quantity + 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

# Route to handle decreasing the quantity of an inventory item
@app.route('/decrease_quantity/<int:id>', methods=['POST'])
def decrease_quantity(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE Inventory SET quantity = quantity - 1 WHERE id = ? AND quantity > 0', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

# Route to handle customer page
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

    # Initialize variables
    flavours = []
    inventory = {}

    if request.method == 'POST':
        search_term = request.form['search']
        cursor = conn.cursor()

        # Fetch flavours matching the search term
        cursor.execute('SELECT * FROM Flavours WHERE flavor_name LIKE ?', ('%' + search_term + '%',))
        flavours = cursor.fetchall()

        # Fetch inventory details for each flavour found
        for flavour in flavours:
            cursor.execute('SELECT * FROM Inventory WHERE flavor_id = ?', (flavour['id'],))
            inventory[flavour['id']] = cursor.fetchall()

        conn.close()

        return render_template('search.html', flavours=flavours, inventory=inventory, search_term=search_term)

    # Ensure to close the database connection in case of GET request or when no search term is provided
    conn.close()

    return render_template('search.html', flavours=flavours, inventory=inventory, search_term='')


# Route to handle submission of suggestion form
@app.route('/submit_suggestion', methods=['POST'])
def submit_suggestion():
    conn = get_db_connection()

    # Fetch form data
    flavor_name = request.form['flavor_name']
    suggestion = request.form['suggestion']
    selected_ingredients = request.form.getlist('inventory')

    # Insert data into Suggestions table (assuming you have a Suggestions table)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Suggestions (flavor_name, suggestion) VALUES (?, ?)',
                   (flavor_name, suggestion))
    suggestion_id = cursor.lastrowid  # Get the ID of the inserted suggestion

    # Insert selected ingredients into InventorySuggestions table (assuming a many-to-many relationship)
    for ingredient_id in selected_ingredients:
        cursor.execute('INSERT INTO InventorySuggestions (suggestion_id, ingredient_id) VALUES (?, ?)',
                       (suggestion_id, ingredient_id))

    conn.commit()
    conn.close()

    # Redirect to a thank you page or any other page after submission
    return redirect(url_for('thank_you'))

# Route for thank you page (optional)
@app.route('/thank_you')
def thank_you():
    return 'Thank you for your suggestion!'




if __name__ == '__main__':
    app.run(debug=True)
