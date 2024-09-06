from flask_app.config.mysqlconnection import connect_to_mysql
from flask_app.models.user import User
from flask import flash




class Product:
    _db = "product_db"

    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.price = data["price"]
        self.description = data["description"]
        self.category = data["category"]
        self.image_url = data["image_url"] 
        self.rating = data["rating"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.users_id = data["users_id"]
        self.user = None

    @staticmethod
    def form_is_valid(form_data):

        is_valid = True

        if len(form_data['title'].strip()) == 0:
            flash("Please enter a product title")
            is_valid = False
        elif len(form_data['title'].strip()) < 2:
            flash("Title must be at least 2 characters")
            is_valid = False

        if len(form_data['price'].strip()) == 0:
            flash("Please enter a price")
            is_valid = False

        if len(form_data['description'].strip()) == 0:
            flash("Please enter a description")
            is_valid = False

        if len(form_data['rating'].strip()) == 0:
            flash("Please enter a rating")
            is_valid = False

        if len(form_data['category'].strip()) == 0:
            flash("Please enter a category")
            is_valid = False

        return is_valid

    @classmethod
    def find_all(cls):

        query = "SELECT * FROM products;"
        list_of_dicts = connect_to_mysql(Product._db).query_db(query)
        products = []

        for each_dict in list_of_dicts:
            product = Product(each_dict)
            products.append(product)

        return products
    
    @classmethod
    def find_all_with_users(cls):

        query = """
        SELECT * FROM products
        JOIN users
        ON products.user_id = users.id;
        """
        list_of_dicts = connect_to_mysql(Product._db).query_db(query)
        products = []

        for each_dict in list_of_dicts:
            product = Product(each_dict)
            user_data = {
                "id": each_dict["users.id"],
                "first_name": each_dict["first_name"],
                "last_name": each_dict["last_name"],
                "email": each_dict["email"],
                "password": each_dict["password"],
                "created_at": each_dict["users.created_at"],
                "updated_at": each_dict["users.updated_at"],
            }
            user = User(user_data)
            product.user = user
            products.append(product)

        return products
    
    @classmethod
    def create(cls, form_data):
        query = """
        INSERT INTO products
        (title, price, description, category, user_id, image_url, rating)
        VALUES
        (%(title)s, %(price)s, %(description)s, %(category)s, %(user_id)s, %(image_url)s, %(rating)s);
        """

        product_id = connect_to_mysql(Product._db).query_db(query, form_data)
        return product_id
    
    @classmethod
    def find_by_id(cls, product_id):
        query = "SELECT * FROM products WHERE id = %s"
        result = connect_to_mysql(cls._db).query_db(query, (product_id,))
        if result:
            return result[0]  
        return None

    @classmethod
    def find_by_id_with_user(cls, product_id):

        query ="""
        SELECT * FROM products
        JOIN users
        ON products.users_id = users.id
        WHERE products.id = %(product_id)s;
        """
        data = {"product_id": product_id}
        list_of_dicts = connect_to_mysql(Product._db).query_db(query, data)
        product = Product(list_of_dicts[0])
        user_data = {
            "id": list_of_dicts[0]['users.id'],
            "first_name": list_of_dicts[0]['first_name'],
            "last_name": list_of_dicts[0]['last_name'],
            "email": list_of_dicts[0]['email'],
            "password": list_of_dicts[0]['password'],
            "created_at": list_of_dicts[0]['users.created_at'],
            "updated_at": list_of_dicts[0]['users.updated_at'],
        }

        user = User(user_data)
        product.user = user
        return product
    
    @classmethod
    def update(cls, form_data):

        query = """
        UPDATE products
        SET
        title = %(title)s,
        price = %(price)s,
        description = %(description)s,
        category = %(category)s,
        image_url = %(image_url)s,
        rating = %(rating)s
        WHERE id = %(product_id)s;
        """

        connect_to_mysql(Product._db).query_db(query, form_data)
        return
    
    @classmethod
    def delete(cls, product_id):

        query = """
        DELETE FROM products
        WHERE id = %(product_id)s;
        """
        data = {"product_id": product_id}
        connect_to_mysql(Product._db).query_db(query, data)
        return

    @classmethod
    def add_to_favorites(cls, user_id, product_id):
        query = "INSERT INTO favorites (user_id, product_id) VALUES (%(user_id)s, %(product_id)s);"
        data = {"user_id": user_id, "product_id": product_id}
        return connect_to_mysql(Product._db).query_db(query, data)

    @classmethod
    def find_favorites_by_user(cls, user_id):
        query = """
            SELECT products.*, favorites.created_at AS favorited_at 
            FROM products 
            JOIN favorites ON products.id = favorites.product_id 
            WHERE favorites.user_id = %(user_id)s;
        """
        data = {"user_id": user_id}
        return connect_to_mysql(Product._db).query_db(query, data)




