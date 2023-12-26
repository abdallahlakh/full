from __init__ import app
from flask import render_template,request,redirect, session,url_for,flash
from __init__ import app
from admin.forms import RegistrationForm, LoginForm,ProductForm,CustomerForm,OrderForm,OrderDetailForm
from admin.database_fonctions import get_recent_orders,get_recent_customers,delete_order_by_id,get_order_by_id,insert_admin,search_for_admin,insert_product, get_products,get_customers,update_product,get_product_by_id,get_customer_by_id,delete_product_by_id,delete_customer_by_id,update_customer,get_orders,update_order


#############adminroutes#########################

















##############loginregister############3
@app.route("/admin/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if  form.validate_on_submit():
        insert_admin(form.username.data,form.email.data,form.password.data)
        return redirect(url_for('home'))
    return render_template('admin/register.html', form=form)



@app.route("/admin/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        exist = search_for_admin(form.username.data, form.password.data)
        
        if exist:
            return redirect(url_for('home'))

    return render_template('/admin/login.html', form=form)


@app.route("/admin/logout")
def logout():
    
    
    # Redirect to the login page or any other appropriate page
    return redirect(url_for('home_customer'))










#########home##################
@app.route('/admin', methods=['GET', 'POST'])
def home():
    products_list = get_products()
    orders_list=get_orders()
    customers_list = get_customers()
    recent_customers_list=get_recent_customers()
    recent_orders_list=get_recent_orders()
    return render_template('admin/admin.html',recent_orders=recent_orders_list,recent_customers=recent_customers_list, products=products_list, customers=customers_list,orders=orders_list)












###################product##########################
@app.route('/admin/addproduct', methods=['GET', 'POST'])
def add_product():
    product_form = ProductForm()
    if request.method == 'POST' and product_form.validate_on_submit():
        # Handle form submission
        insert_product(
            product_form.category.data,
            product_form.title.data,
            product_form.price.data,
            product_form.description.data,
            product_form.features.data
        )
        flash('Product added successfully!')
        return redirect(url_for('home'))

    return render_template('admin/add_product.html', product_form=product_form)

@app.route('/admin/editproduct/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = get_product_by_id(product_id)
    product_form = ProductForm()
    if request.method == 'POST' and product_form.validate_on_submit():
        update_product(
            product_id,
            product_form.category.data,
            product_form.title.data,
            product_form.price.data,
            product_form.description.data,
            product_form.features.data
        )
        flash('Product updated successfully!')
        return redirect(url_for('home'))

    return render_template('admin/edit_product.html', product_form=product_form, product=product)



@app.route('/admin/seeproduct/<int:product_id>', methods=['GET'])
def see_product(product_id):
    product = get_product_by_id(product_id)
    product_form = ProductForm()
    return render_template('admin/see_product.html', product_form=product_form, product=product)




@app.route('/admin/deleteproduct/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    delete_product_by_id(product_id)
    return redirect(url_for('home'))













################customer###########################
@app.route('/admin/editcustomer/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customer = get_customer_by_id(customer_id)
    print(customer)
    customer_form = CustomerForm()

    if request.method == 'POST' and customer_form.validate_on_submit():
        # Handle form submission for editing the customer
        update_customer(
            customer_id,
            customer_form.email.data,
            customer_form.first_name.data,
            customer_form.last_name.data,
            customer_form.registration_date.data,
            customer_form.last_login.data,
            customer_form.is_active.data
        )
        flash('Customer updated successfully!')
        return redirect(url_for('home'))

    return render_template('admin/edit_customer.html', customer_form=customer_form, customer=customer)

@app.route('/admin/deletecustomer/<int:customer_id>')
def delete_customer(customer_id):
    delete_customer_by_id(customer_id)
    return redirect(url_for('home'))


@app.route('/admin/seecustomer/<int:customer_id>', methods=['GET'])
def see_customer(customer_id):
    customer = get_customer_by_id(customer_id)
    registration_date_str = customer[5].strftime('%Y-%m-%d %H:%M:%S')
    last_login_str = customer[6]
    customer_form = CustomerForm(
        email=customer[1],
        first_name=customer[3],
        last_name=customer[4],
        registration_date=registration_date_str,
        last_login=last_login_str,
        is_active=str(customer[7])  
    )

    return render_template('admin/see_customer.html', customer_form=customer_form, customer=customer)










##############order########################




@app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
       order = get_order_by_id(order_id)
       form = OrderForm(obj=order)
       if request.method == 'POST':
         order_data=[form.order_status.data,form.payment_method.data,order_id]
         update_order(order_data)
         return redirect(url_for('home'))
       return render_template('admin/edit_order.html', order=order, form=form)




@app.route('/delete_order/<int:order_id>')
def delete_order(order_id):
    delete_order_by_id(order_id)  # Implement the delete_order_by_id function
    return redirect(url_for('home'))





@app.route('/see_order/<int:order_id>')
def see_order(order_id):
    # Implement the get_order_by_id function
    order = get_order_by_id(order_id)
    # Create instances of the forms and populate them with order data
    order_form = OrderForm(
        customer_id=order['order_info'][1],
        order_date= order['order_info'][2],
        total_amount= order['order_info'][3],
        order_status= order['order_info'][4],
        payment_method= order['order_info'][5],
    )

    # Adjust the order details form data based on your provided structure
    order_detail_forms = [OrderDetailForm(
        product_id=detail[1],
        quantity= detail[2],
        price_per_unit=detail[3],
        subtotal= detail[4],
    ) for detail in order['order_details']]

    # Render the template with order details
    return render_template('admin/see_order.html', order=order, order_form=order_form, order_detail_forms=order_detail_forms)



######################endadminroutes#######################################










######################customerroutes############################################


from customer.forms import CustomerLoginForm,CustomerRegistrationForm
from customer.database_fonctions import search_for_customer,get_categories,select_product_according_to_category,get_product_by_id,insert_product_to_shoppingcart,get_shopping_cart_data,get_product_price,clear_shopping_cart,insert_order_and_details,insert_customer
from collections import defaultdict

##############loginregister############3

@app.route("/customer/register", methods=['GET', 'POST'])
def register_customer():
    form = CustomerRegistrationForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        insert_customer(first_name, last_name, email, password)
        categories = get_categories()
        is_login=[True if session['customer_id'] != None else False ]
        return render_template('customer/customer.html', categories=categories, is_login=is_login)



    return render_template('customer/register.html', form=form)



@app.route("/customer/login", methods=['GET', 'POST'])
def login_customer():
    form = CustomerLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        exists, customer_id = search_for_customer(form.username.data, form.password.data)

        if exists:
            session['customer_id'] = customer_id

            # Update categories after successful login
            categories = get_categories()
            is_login = session.get('customer_id') is not None

            return render_template('customer/customer.html', categories=categories, is_login=is_login)

        else:
            flash(f'Account does not exist for {form.username.data}!')

    return render_template('/customer/login.html', form=form)

@app.route("/")
def logout_customer():
    session['customer_id'] = None
    categories = get_categories()
    is_login = session.get('customer_id') is not None
    print(session['customer_id'])
    return render_template('customer/customer.html', categories=categories, is_login=is_login)




@app.route('/', methods=['GET', 'POST'])

#----------home--------------
def home_customer():
    categories = get_categories()
    is_login=[True if session['customer_id'] != None else False ]
    return render_template('customer/customer.html', categories=categories, is_login=is_login)
#-----------end---------------








#-------------for rendering template according to what user chose from gallery-----
@app.route('/customer/products/<category>')
def product_category(category):
    products_category=select_product_according_to_category(category)
    return render_template(f'customer/products/{category}.html',products=products_category)
#-----------------------end---------------------------



#--------------rendering product details from product_category------
@app.route('/customer/products/<int:product_id>')
def product_detail(product_id):
    product = get_product_by_id(product_id)
    return render_template('customer/productdetail.html',product=product)
#----------------------end---------------










#-------add product to cart from productdetails---------------
@app.route('/customer/add_cart/<int:product_id>/<float:price>', methods=['GET', 'POST'])
def add_cart(product_id, price):
    try:
        is_login = session.get('customer_id') is not None 
        if is_login:
            insert_product_to_shoppingcart(session['customer_id'], product_id, price)
            session.modified = True  
        categories = get_categories()
        is_login=[True if session['customer_id'] != None else False ]
        return render_template('customer/customer.html', categories=categories, is_login=is_login)

    except Exception as e:
        print(f"Error: {e}")
        flash('An error occurred while adding the product to the shopping cart.')
        return redirect(url_for('home_customer'))
#------------end----------------








#---------shopppingcart------------
from flask import render_template, redirect, url_for, session
from collections import defaultdict

@app.route('/customer/shopping_cart', methods=['GET', 'POST'])
def shopping_cart():
    if request.method == 'POST':
        # Assuming you have a function to generate an order ID (replace it with your own logic)

        # Assuming you have a function to get the current date and time (replace it with your own logic)
    
        payment_method = request.form.get('payment_method')
        # Get the customer ID from the session
        customer_id = session.get('customer_id')

        # Assuming you have a function to fetch the shopping cart data
        shopping_cart_data = get_shopping_cart_data(customer_id)

        # Group the shopping cart data by product_id and calculate the total quantity
        grouped_cart_data = defaultdict(int)
        for item in shopping_cart_data:
            _, _, product_id, quantity, _, _, _ = item
            grouped_cart_data[product_id] += quantity

        # Convert the grouped data back to a list of tuples with subtotal
        grouped_cart_list = []
        total = 0
        for product_id, quantity in grouped_cart_data.items():
            # Assuming you have a function to get the product price based on the product_id
            product_price = get_product_price(product_id)

            if product_price is not None:
                subtotal = quantity * product_price
                total += subtotal
                grouped_cart_list.append((product_id, quantity, product_price, subtotal))

        # Assuming you have a function to clear the shopping cart for the customer
        clear_shopping_cart(customer_id)

        # Assuming you have a function to insert the order and order details into the database
        insert_order_and_details(customer_id, total, grouped_cart_list,payment_method)
        categories = get_categories()
        is_login=[True if session['customer_id'] != None else False ]
        return render_template('customer/customer.html', categories=categories, is_login=is_login)


    else:
        # Render the shopping cart page as usual
        shopping_cart_data = get_shopping_cart_data(session['customer_id'])
        grouped_cart_data = defaultdict(int)
        for item in shopping_cart_data:
            _, _, product_id, quantity, _, _, _ = item
            grouped_cart_data[product_id] += quantity
        grouped_cart_list = []
        total = 0

        for product_id, quantity in grouped_cart_data.items():
            product_price = get_product_price(product_id)
            if product_price is not None:
                subtotal = quantity * product_price
                total += subtotal
                grouped_cart_list.append((product_id, quantity, product_price, subtotal))

        return render_template('customer/shoppingcard.html', shopping_cart=grouped_cart_list, total=total)

#------------------end---------------------














if __name__=="__main__":
    app.run(debug=True)