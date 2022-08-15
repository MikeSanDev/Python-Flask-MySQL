from flask import Flask, session

app = Flask(__name__)
app.secret_key = "spicy tacos"
db_name = 'login_reg'
