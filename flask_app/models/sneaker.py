# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app


class Sneaker:
    db = 'snkrs_site'
    
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.name2 = data['name2']
        self.brand = data['brand']
        # self.image = data['image'] maybe insert HTML element assign image dynamically
        self.colorway = data['colorway']
        self.style = data['style']
        self.release_date = data['release_date']
        self.retail_price = data['retail_price']
        self.description = data['description']
        self.price = data['price']
        # self.size = data['size']
        self.stock = {
            # self.stock at [0] stores how many in stock, and indices after stores their in_stock id's
            '7':    [0],
            '7.5':  [0],
            '8':    [0],
            '8.5':  [0],
            '9':    [0],
            '9.5':  [0],
            '10':   [0],
            '10.5': [0],
            '11':   [0],
            '11.5': [0],
            '12':   [0],
            '12.5': [0],
            '13':   [0],
            '13.5': [0]
        }

    # -----------------------------------------------------------------------------
    # READ
    # -----------------------------------------------------------------------------

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sneaker;"
        # Make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db).query_db(query)
        # Create an empty list to append our instances of sneakers
        if(results):
            sneakers = []
            # Iterate over the db results and create instances of sneakers with cls.
            for row in results:
                sneakers.append(cls(row))
            return sneakers

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM sneaker WHERE id = %(id)s;"

        result = connectToMySQL(cls.db).query_db(query, data)
        if(result):
            return cls(result[0])

    @classmethod
    def get_stock_by_id(cls, data):
        query = "SELECT * FROM sneaker "\
                "LEFT JOIN in_stock ON in_stock.sneaker_id = sneaker.id "\
                "WHERE sneaker.id = %(id)s"
        # Make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db).query_db(query, data)
        # Create an empty list to append our instances of sneakers
        if(results):
            sneaker = cls(results[0])
            # print(sneaker)
            # Iterate over the db results and create instances of sneakers with cls.
            if results[0]['size']:
                for row in results:
                    sneaker.stock[row['size']][0] += 1
                    sneaker.stock[row['size']].append(row['in_stock.id'])
                return sneaker
            
            else:
                sneaker.flash = "Out of Stock"
                return sneaker

    # -----------------------------------------------------------------------------
    # Add to Cart
    # -----------------------------------------------------------------------------
    @classmethod
    def add_to_cart(cls, data):
        query = "INSERT INTO cart (user_id, in_stock_id, created_at) " \
                "VALUES (%(user_id)s, %(in_stock_id)s, NOW())"

        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_from_cart(cls, data):
        query = "DELETE FROM cart WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)