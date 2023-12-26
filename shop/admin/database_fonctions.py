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










#---------------------admin fonctions----------------------------

def insert_admin(username, email, password):
    connection = connect_to_database()
    cursor = connection.cursor()

    # Assuming you have a table named 'users'
    query = "INSERT INTO admin (username, email, password) VALUES (%s, %s, %s)"
    values = (username, email, password)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()


def search_for_admin(username, password):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT * FROM admin WHERE username = %s AND password = %s"
    values = (username, password)
    cursor.execute(query, values)
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    return True if user else False

#-------------------end------------------------------------
















#-----------------product fonctions-------------------------



#-------------------------get--------------------------------------
def get_products():
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM product"
    cursor.execute(query)
    products = cursor.fetchall()
    for product in products:
       query = "SELECT category_name FROM product_category where product_category.category_id=%s"
       value=(product['category_id'],)
       cursor.execute(query, value)
       product_category = cursor.fetchall()
       product['category_id']=product_category[0]
    cursor.close()
    connection.close()

    return products
#------------------------------------------------------




#--------------------------get id -------------------
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
        pf.feature_description  
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
            'features': [feature[5] for feature in result if feature[5]]
        }
        return product
    else:
        return None
#---------------------------------------------------------------







#-------------------------insert-------------------------
def insert_product(category, title, price, description, features):
    connection = connect_to_database()
    cursor = connection.cursor()
    selecting = "SELECT category_id FROM product_category WHERE category_name = %s"
    value = (category,)
    cursor.execute(selecting, value)
    category_id = cursor.fetchone()[0]
    query = "INSERT INTO product (category_id, product_title, price, product_description) VALUES (%s, %s, %s, %s)"
    values = (category_id, title, price, description)
    cursor.execute(query, values)
    connection.commit()
    product_id = cursor.lastrowid
    feature_list = features.split(',')
    feature_query = "INSERT INTO product_features (product_id, feature_description) VALUES (%s, %s)"
    feature_values = [(product_id, feature) for feature in feature_list]

    cursor.executemany(feature_query, feature_values)
    connection.commit()

    cursor.close()
    connection.close()
#---------------------------------------------------------------









#--------------------update-----------------
def update_product(product_id, category, title, price, description, features):
    connection = connect_to_database()
    cursor = connection.cursor()
    selecting = "SELECT category_id FROM product_category WHERE category_name = %s"
    value = (category,)
    cursor.execute(selecting, value)
    category_id = cursor.fetchone()[0]
    query = "UPDATE product SET category_id=%s, product_title=%s, price=%s, product_description=%s WHERE product_id=%s"
    values = (category_id, title, price, description, product_id)
    cursor.execute(query, values)
    connection.commit()
    delete_query = "DELETE FROM product_features WHERE product_id = %s"
    cursor.execute(delete_query, (product_id,))
    connection.commit()
    feature_list = features.split(',')
    print(feature_list)
    feature_query = "INSERT INTO product_features (product_id, feature_description) VALUES (%s, %s)"
    feature_values = [(product_id, feature) for feature in feature_list]
    cursor.executemany(feature_query, feature_values)
    connection.commit()
    cursor.close()
    connection.close()

#-----------------------delete----------------------

def delete_product_by_id(product_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT order_id FROM order_details WHERE product_id=%s"
    value = (product_id,)
    cursor.execute(query, value)
    result = cursor.fetchone()
    if result:
        order_id = result[0]
        query = "SELECT COUNT(*) FROM order_details WHERE order_id=%s"
        value = (order_id,)
        cursor.execute(query, value)
        number_of_orders_per_product = cursor.fetchone()[0]
        if number_of_orders_per_product == 1:
            cursor.execute("DELETE FROM order_details WHERE order_id=%s", (order_id,))
            cursor.execute("DELETE FROM orders WHERE OrderID=%s", (order_id,))
            cursor.execute("DELETE FROM product_features WHERE product_id = %s", (product_id,))
            cursor.execute("DELETE FROM product WHERE product_id = %s", (product_id,))
 
        elif number_of_orders_per_product > 1:
            cursor.execute("DELETE FROM order_details WHERE order_id=%s and product_id=%s", (order_id,product_id))
            cursor.execute("DELETE FROM product_features WHERE product_id = %s", (product_id,))
            cursor.execute("DELETE FROM product WHERE product_id = %s", (product_id,))
        connection.commit()
    else:
        print("There is no order for this product.")
        print(product_id)
        cursor.execute("DELETE FROM product_features WHERE product_id = %s", (product_id,))
        cursor.execute("DELETE FROM product WHERE product_id = %s", (product_id,))
        connection.commit()
    cursor.close()
    connection.close()






















#--------------------costumer fonctions----------------------
    


#------------------get------------------------------------
def get_customers():
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM customers"
    cursor.execute(query)
    customers = cursor.fetchall()

    cursor.close()
    connection.close()

    return customers
#-----------------------------------------------------------

#----------------get id------------------
def get_customer_by_id(customer_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT * FROM customers WHERE customer_id = %s"
    cursor.execute(query, [customer_id])
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    return result
#---------------------------------------update------------------

def update_customer(customer_id, email, first_name, last_name, registration_date, last_login, is_active):
    connection = connect_to_database()
    cursor = connection.cursor()
    query = "UPDATE customers SET email=%s, first_name=%s, last_name=%s, registration_date=%s, last_login=%s, is_active=%s WHERE customer_id=%s"
    values = (email, first_name, last_name, registration_date, last_login, is_active, customer_id)
    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

#--------------------------------------------


#-------------------delete-----------------------
def delete_customer_by_id(customer_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        print(f"Deleting customer with ID: {customer_id}")
        cursor.execute("DELETE FROM customers WHERE customer_id =%s", (customer_id,))

        connection.commit()
        flash('Customer deleted successfully!', 'success')  # Specify the category as 'success'
        print("Deletion successful")
    except Exception as e:
        flash(f'Error deleting customer: {str(e)}', 'error')  # Specify the category as 'error'
        print(f"Error deleting customer: {str(e)}")
    finally:
        cursor.close()
        connection.close()



#--------------end------------------
        


















#-------------------order fonction--------------------------



def get_orders():
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM orders "

    cursor.execute(query)
    orders = cursor.fetchall()
    print(orders)

    cursor.close()
    connection.close()

    return orders


def get_order_by_id(order_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    # Retrieve from the orders table
    cursor.execute("SELECT * FROM orders WHERE OrderID = %s", (order_id,))
    order_result = cursor.fetchone()

    # Retrieve from the order_details table
    cursor.execute("SELECT * FROM order_details WHERE order_id = %s", (order_id,))
    order_details_result = cursor.fetchall()

    cursor.close()
    connection.close()

    # Combine results from both tables
    order = {
        "order_info": order_result,
        "order_details": order_details_result
    }

    return order



def delete_order_by_id(order_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        # Delete from the orders table
        cursor.execute("DELETE FROM order_details WHERE order_id = %s", (order_id,))

        cursor.execute("DELETE FROM orders WHERE OrderID = %s", (order_id,))
        
        # Delete from the order_details table

        connection.commit()
    except Exception as e:
        print(f"Error deleting order: {str(e)}")
    finally:
        cursor.close()
        connection.close()


def update_order(order_data):
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        # Update order information
        update_order_query = """
            UPDATE orders
            SET
                order_status = %s,
                payment_method = %s
            WHERE
                OrderID = %s
        """
        cursor.execute(update_order_query, (order_data[0],order_data[1],order_data[2]))
        connection.commit()

        # # Update order details
        # update_order_details_query = """
        #     UPDATE order_details
        #     SET
        #         product_id = %s,
        #         quantity = %s,
        #         price_per_unit = %s,
        #         subtotal = %s
        #     WHERE
        #         order_detail_id = %s
        # """
        # for detail_info in order_data['order_details']:
        #     cursor.execute(update_order_details_query, detail_info)
        # connection.commit()

    except Exception as e:
        # Handle exceptions, log errors, rollback changes if necessary
        print(f"Error updating order: {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()












#----------------------dashboard fonction--------------------------

def get_recent_customers():
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    # Calculate the date 3 days ago
    three_days_ago = datetime.now() - timedelta(days=3)

    query = "SELECT * FROM customers WHERE registration_date >= %s"
    cursor.execute(query, (three_days_ago,))
    customers = cursor.fetchall()

    cursor.close()
    connection.close()

    return customers


def get_recent_orders():
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    # Calculate the date 3 days ago
    three_days_ago = datetime.now() - timedelta(days=3)

    query = "SELECT * FROM orders WHERE order_date >= %s"
    cursor.execute(query, (three_days_ago,))
    orders = cursor.fetchall()

    cursor.close()
    connection.close()

    return orders
