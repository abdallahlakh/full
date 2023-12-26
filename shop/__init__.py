from flask import Flask


app=Flask(__name__)





app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'ecommerce'
app.config['SECRET_KEY'] = '231fc9d70372e072a1e616dee0feb5f3'



