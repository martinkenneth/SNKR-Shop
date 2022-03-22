# import the function that will return an instance of a connection
import imp
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models import sneaker
import re

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$')


class User:
    db = 'snkrs_site'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # -----------------------------------------------------------------------------
    # CREATE
    # -----------------------------------------------------------------------------

    @classmethod
    def create(cls, data):
        # run bcrypt within create() to generate hash for password
        hashed = bcrypt.generate_password_hash(data['password'])

        user = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'password': hashed,
        }
        query = "INSERT INTO user (first_name, last_name, email, password, created_at) "\
                "VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW());"
        return connectToMySQL(cls.db).query_db(query, user)

    # -----------------------------------------------------------------------------
    # READ
    # -----------------------------------------------------------------------------

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"

        result = connectToMySQL('belt_exam_car_deals').query_db(query, data)
        if(result):
            return cls(result[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result)
        if(result):
            return cls(result[0])

    @classmethod
    def get_users_cart(cls, data):
        query = "SELECT * FROM cart "\
                "LEFT JOIN user on user.id = cart.user_id "\
                "LEFT JOIN in_stock on in_stock.id = cart.in_stock_id "\
                "LEFT JOIN sneaker on sneaker.id = in_stock.sneaker_id "\
                "WHERE user.id = %(id)s;"
        # Make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('snkrs_site').query_db(query, data)

        # Create an empty list to append our instances of sneakers
        if(results):
            user = cls(results[0])

            user.cart = []

            for row in results:
                data = {
                    'id'            :row['sneaker_id'],
                    'name'          :row['name'],
                    'name2'         :row['name2'],
                    'brand'         :row['brand'],
                    'colorway'      :row['colorway'],
                    'style'         :row['style'],
                    'release_date'  :row['release_date'],
                    'retail_price'  :row['retail_price'],
                    'description'   :row['description'],
                    'price'         :row['price'],
                    'size'          :row['size']
                }
                sneaker_ = sneaker.Sneaker(data)
                sneaker_.size = row['size']
                sneaker_.cart_id = row['id']
                print(sneaker_.name)
                print(sneaker_.size)
                user.cart.append(sneaker_)
            return user

    # -----------------------------------------------------------------------------
    # @staticmethod to validate our User attributes prior to querying
    # -----------------------------------------------------------------------------
    @staticmethod
    def validate_registration(user):
        # First Name - letters only, at least 2 characters and that it was submitted
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.", 'invalid name')
            is_valid = False
        # Last Name - letters only, at least 2 characters and that it was submitted
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.", 'invalid name')
            is_valid = False
        # Email - valid Email format, does not already exist in the database, and that it was submitted
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", 'invalid email')
            is_valid = False
        if(User.get_by_email(user)):
            flash("This email exists already.", 'invalid email')
            is_valid = False
        # Password - at least 8 characters, and that it was submitted
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", 'invalid password')
            is_valid = False
        # Password Confirmation - matches password
        if user['password'] != user['password2']:
            flash("Passwords do not match.", 'invalid password match')
            is_valid = False
        if not PASSWORD_REGEX.match(user['password']):
            flash("Password must contain at least 1 "
                  "number and 1 uppercase letter.", 'invalid password')
            is_valid = False

        return is_valid


    @staticmethod
    def validate_login(user):
        # print(user)
        is_valid = True

        if not(user['email']) or not(user['password']) or not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email/Password.", "login")
            is_valid = False
        else:
            user_in_db = User.get_by_email(user)
            if not user_in_db:
                print("enter email check")
                flash("Invalid Email/Password.", "login")
                is_valid = False
            if user_in_db:
                if not (bcrypt.check_password_hash(user_in_db.password, user['password'])):
                    flash("Invalid Email/Password.", "login")
                    is_valid = False
                    
        if is_valid:
            session['user_id'] = user_in_db.id

        return is_valid
