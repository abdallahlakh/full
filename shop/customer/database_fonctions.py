from curses import flash
import mysql.connector
from flask import flash
from datetime import datetime, timedelta

def connect_to_database():
    # Modify these values with your actual database credentials
    config = {
        'user': 'root',
        'password': '1234',
        'host': 'localhost',
        'database': 'ecommerce',
        'raise_on_warnings': True,
    }
    connection = mysql.connector.connect(**config)
    return connection
from datetime import datetime

def insert_customer(first_name, last_name, email, password):
    # Assuming you have a database connection
    connection = connect_to_database()
    cursor = connection.cursor()

    # Assuming your 'customers' table has columns (customer_id, email, password_hash, first_name, last_name, registration_date, last_login, is_active)
    query = """
        INSERT INTO customers (email, password_hash, first_name, last_name, registration_date, last_login, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (email, password, first_name, last_name, str(datetime.utcnow()), None, True)  # Adjust the default values accordingly

    try:
        cursor.execute(query, values)
        connection.commit()
    except Exception as e:
        print(f"Error inserting customer: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

def search_for_customer(username, password):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT * FROM customers WHERE first_name = %s AND password_hash = %s"
    values = (username, password)
    cursor.execute(query, values)
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    # Return user as a tuple or None if not found
    return (True, user[0]) if user else (False, None)

def get_categories():
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT category_name,image_url FROM product_category "
    cursor.execute(query)
    data= cursor.fetchall()
    cursor.close()
    connection.close()
    return data

def select_product_according_to_category(category):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT category_id FROM product_category where category_name=%s"
    cursor.execute(query, (category,))
    id= cursor.fetchone()
    query2 = "SELECT * FROM product where category_id=%s"
    cursor.execute(query2, id)
    data=cursor.fetchall()
    return data



def get_product_by_id(product_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    
    query = """
    SELECT 
        p.product_id, 
        pc.category_name, 
        p.product_title, 
        p.price, 
        p.product_description, 
        pf.feature_description,
        p.image_url 
    FROM 
        product p, 
        product_category pc, 
        product_features pf 
    WHERE 
        p.product_id = %s 
        AND pc.category_id = p.category_id 
        AND pf.product_id = p.product_id
"""
    cursor.execute(query, [product_id])
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()

    if result:
        product = {
            'product_id': result[0][0],
            'category_name': result[0][1],
            'product_title': result[0][2],
            'price': result[0][3],
            'product_description': result[0][4],
            'features': [feature[5] for feature in result if feature[5]],
            'image_url':result[0][6]
        }
        return product
    else:
        return None
    

def insert_product_to_shoppingcart(customer_id, product_id, price):
    connection = connect_to_database()
    cursor = connection.cursor()

    query = """
    INSERT INTO shopping_cart (customer_id, product_id, quantity, price, timestamp, status)
    VALUES (%s, %s, 1, %s, CURRENT_TIMESTAMP, 'active')
    """
    values = (customer_id, product_id, price)

    try:
        cursor.execute(query, values)
        connection.commit()
        print("Product added to the shopping cart successfully!")
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()
    return
def get_shopping_cart_data(customer_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        # Fetch shopping cart data for a specific customer
        query = "SELECT * FROM shopping_cart WHERE customer_id = %s"
        cursor.execute(query, (customer_id,))
        shopping_cart_data = cursor.fetchall()

        return shopping_cart_data

    except Exception as e:
        # Handle the exception (log, print, etc.)
        print(f"Error fetching shopping cart data: {e}")
        return None

    finally:
        cursor.close()
        connection.close()




def get_product_price(product_id):
    # Assuming you have a database connection
    connection = connect_to_database()
    cursor = connection.cursor()

    # Assuming you have a table named 'products' with columns 'product_id' and 'price'
    query = "SELECT price FROM product WHERE product_id = %s"
    values = (product_id,)

    try:
        cursor.execute(query, values)
        result = cursor.fetchone()

        if result:
            return result[0]  # Assuming price is the first column in the result
        else:
            return None  # Handle the case where the product_id doesn't exist

    except Exception as e:
        print(f"Error fetching product price: {e}")
        return None

    finally:
        cursor.close()
        connection.close()



def clear_shopping_cart(customer_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        # Assuming you have a table named 'shopping_cart'
        delete_query = "DELETE FROM shopping_cart WHERE customer_id = %s"
        delete_values = (customer_id,)
        cursor.execute(delete_query, delete_values)
        connection.commit()

    except Exception as e:
        print(f"Error clearing shopping cart: {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()




from datetime import datetime

def insert_order_and_details(customer_id, total, grouped_cart_list,payment_method):
    # Get the current date and time
    order_date = datetime.now()

    # Assuming you have a database connection
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        # Insert into the orders table
        orders_query = "INSERT INTO orders (customer_id, order_date, total_amount, order_status,payment_method) VALUES (%s, %s, %s, %s,%s)"
        orders_values = (customer_id, order_date, total, 'pending',payment_method)
        cursor.execute(orders_query, orders_values)
        connection.commit()

        # Get the last inserted order ID
        last_order_id = cursor.lastrowid

        # Insert into the order_details table
        order_details_query = "INSERT INTO order_details (product_id, quantity, price_per_unit, subtotal, order_id) VALUES (%s, %s, %s, %s, %s)"
        for item in grouped_cart_list:
            product_id, quantity, product_price, subtotal = item
            order_details_values = (product_id, quantity, product_price, subtotal, last_order_id)
            cursor.execute(order_details_query, order_details_values)

        connection.commit()

    except Exception as e:
        print(f"Error inserting order and details: {e}")
        connection.rollback()


    finally:
        cursor.close()
        connection.close()
