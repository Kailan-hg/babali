from datetime import date
from django.db import models
import psycopg2
from django.core.validators import MinValueValidator


class BuyerProduct(models.Model):
    _id = None
    _id_product = None
    _username = models.CharField(max_length=30)
    _status = models.CharField(max_length=30)
    _price = models.CharField(max_length=30)
    _product = models.CharField(max_length=30)
    _company_name = models.CharField(max_length=30)
    _date_sold = None

    # var to database.
    _conn = None
    # Cursor this connection.
    _cur = None
    # Lines recovery cursor.
    _rows = None

    # CONST
    _BUYERPRODUCTTABLE = "buyer_products"
    _MAKERPRODUCTTABLE = "maker_products"
    _BUYERUSERTABLE = "buyer_user"

    # Public
    error = []
    success = []

    def __init__(self, username=None, id_product=None):
        # Assing principal vars
        self._username = username
        self._date_sold = date.today()
        self._status = "Pendiente"
        self._id_product = id_product
        # Database conection.
        self._conn = psycopg2.connect(
            database="babali",
            user="hernani",
            password="03031516h",
            host="localhost",
            port="5432"
        )

        # Cursor this conection
        self._cur = self._conn.cursor()

    def _user_validate(self):
        # Validate user exist
        query = f"SELECT * FROM {self._BUYERUSERTABLE} WHERE username='{self._username}'"
        try:
            self._cur.execute(query)
            self._rows = self._cur.fetchone()
            # User exist in database
            if None is not self._rows:
                self.success.append("Usuario encontrado")
                return True
            # User not found
            else:
                self.error.append("Usuario no existente")
                return False
        # Error connection in database
        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")
            # Finish connection with database
            self._conn.close()

    def send_request(self):
        self._product_validate()

    def _product_validate(self):
        # Query the search to product in database maker_product
        query = f"SELECT * FROM {self._MAKERPRODUCTTABLE} WHERE id='{self._id_product}'"
        try:
            self._cur.execute(query)
            self._rows = self._cur.fetchone()
            if None is not self._rows:
                # Check stuck product
                if self._rows[4] > 0:  # [4] amount_stuck
                    # assing var is product
                    self._price = self._rows[3]  # price_und
                    self._company_name = self._rows[6]  # amount_sold
                    self._product = self._rows[1]  # product
                    self._state = "En progreso"
                    self.success.append("Tenemos stuck")
                    return True
                # Not product stuck
                else:
                    self.error.append("No tenemos stuck")
                    return False
            # Id_product not found in database
            else:
                self.error.append("El product no existe")
                return False
        # Error connection in database
        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")
            # Finish connection with database
            self._conn.close()

    def _send_db(self):
        # Query to insert product in database
        query = f"""INSERT INTO {self._BUYERPRODUCTTABLE}(status, price, product, date_sold, username, id_product)
        values ('{self._status}', '{self._price}', '{self._product}', '{self._date_sold}', '{self._username}', '{self._id_product}')"""

        try:
            # execute and push query
            self._cur.execute(query)
            self._id = self._cur.lastrowid
            self._conn.commit()
            self.success.append("El producto a sido agregado al carrito")
        # Error conection in database
        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")
            # Finish connection with database
            self._conn.close()
            return False

    def trolley_check(self):
        query = f"SELECT * FROM {self._BUYERPRODUCTTABLE} WHERE username='{self._username}'"
        try:
            self._cur.execute(query)
            self._rows = self._cur.fetchall()
            if None is not self._rows:
                self.success.append("Se encontraron productos")
                return self._rows
            else:
                self.error.append("Aun no has agregado productos al carrito")
        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")
            # Finish connection with database
            self._conn.close()
            return False

    def trolley_buy(self, id):
        self._state = "Compra finalizada"
        query = f"UPDATE {self._BUYERPRODUCTTABLE} SET state='{self._state}' WHERE id='{id}'"

        try:
            self._cur.execute(query)
            self._conn.commit()
            self.success.append("Se compraron los productos")
        # Database error connection
        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")
            # Finish connection with database
            self._conn.close()
            return False

    # Generar graficos
    def return_products_by_user(self):
        query = f"SELECT * FROM {self._BUYERPRODUCTTABLE} WHERE company_name='{self._username}'"

        try:
            self._cur.execute(query)
            self._rows = self._cur.fetchall()
            return self._rows
        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")
            # Finish connection with database
            self._conn.close()
            return False


class MakerProduct():
    _company_name = None
    _product = None
    _amount = None
    _price_und = None
    _amount_stuck = None
    _amount_sold = None

    # var to database.
    _conn = None
    # Cursor this connection.
    _cur = None
    # Lines recovery cursor.
    _rows = None

    # CONST
    _BUYERPRODUCTTABLE = "buyer_products"
    _MAKERPRODUCTTABLE = "maker_products"
    _MAKERUSERTABLE = "maker_user"

    success = []
    error = []

    def __init__(self, company_name=None):
        self._company_name = company_name

        # Database connect
        self._conn = psycopg2.connect(
            database="babali",
            user="hernani",
            password="03031516h",
            host="localhost",
            port="5432"
        )

        # Cursor this conection
        self._cur = self._conn.cursor()

    """
        TODO : Save values to product receive to method: POST (Created product)
        @params : product, amount, price_und, amount_stuck, amount_sold
    """

    def save_product(self, product, amount, price_und, amount_stuck, amount_sold):
        self._product = product
        self._amount = amount
        self._price_und = price_und
        self._amount_stuck = amount_stuck
        self._amount_sold = amount_sold

        self.success.append("Se guardaron los datos")

    """
        TODO : Insert values to database.
        Execute save_product before to this function.
    """

    def save_request(self):
        if self._product is not None and self._amount is not None and self._price_und is not None and self._amount_stuck is not None and self._amount_sold is not None:
            if self._new_product():
                self.success = "Se insertaron los productos"
                return True
            else:
                self.error.append(
                    "Verifique los valores, no se pueden enviar ningun valor: \"None\"")
                return False

    def _new_product(self):
        query = f"""INSERT INTO {self._MAKERPRODUCTTABLE}(product, amount, price_und, amount_stuck, amount_sold, company_name)
        VALUES('{self._product}', {self._amount}, {self._price_und}, {self._amount_stuck}, {self._amount_sold}, '{self._company_name}')
        """

        # Execute and validate error log.
        try:
            self._cur.execute(query)
            self._conn.commit()
            return True
        # Error in database, close connection.
        except psycopg2.DatabaseError as e:
            self.error.append(f"error: {e}")
            self._conn.close()
            return False


class NewProductForm (models.Model):
    product = models.CharField(max_length=100)
    amount = models.IntegerField(validators=[MinValueValidator(0)])
    price_und = models.IntegerField(validators=[MinValueValidator(1)])
    amount_stuck = models.IntegerField(validators=[MinValueValidator(0)])
    amount_sold = models.IntegerField(validators=[MinValueValidator(0)])
    company_name = models.CharField(max_length=3000)
