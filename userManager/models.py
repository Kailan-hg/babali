# Settings and libraries import.
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.http import HttpResponse
from datetime import date
import psycopg2
import http.cookies


class Buyer(models.Model):
    """
        Buyer administrative class.
        @params: username, password, email, first_name, last_name => basically config to database.
        methods to administrative user:
            set user in database
            check user in database
            push user in database
    """
    _id = None
    _username = models.CharField(max_length=30, unique=True, validators=[
                                 ASCIIUsernameValidator()])
    _password = models.CharField(max_length=30, validators=[
                                 UnicodeUsernameValidator()])
    _email = models.EmailField(unique=True)
    _first_name = models.CharField(max_length=30)
    _last_name = models.CharField(max_length=30)
    _date = None

    # var to database.
    _connection = None
    # Cursor this connection.
    _cur = None
    # Lines recovery cursor.
    _rows = None

    # CONST
    _BUYERTABLE = "Buyer"
    _BUYERUSERTABLE = "buyer_user"

    # Public
    error = []

    def __init__(self, username=None, password=None, email=None, first_name=None, last_name=None):
        self._username = username
        self._password = password
        self._email = email
        self._first_name = first_name
        self._last_name = last_name
        self._date = date.today()

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

    # Save user the database
    def _save_db(self):
        # query to insert user.
        query = f"""
        INSERT INTO {self._BUYERUSERTABLE}(username, password, email, first_name, last_name, date_requested)
        VALUES ('{self._username}', '{self._password}', '{self._email}', '{self._first_name}', '{self._last_name}',
        '{self._date}')
        """
        # Validate insert
        try:
            # Execute query in database
            self._cur.execute(query)
            # Push user db
            self._conn.commit()

        # Validate error and push in self.error[]
        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")

    # Public method: save in database, check errors and validate info

    def request_save(self):
        try:
            # Check if user to exist in database.
            if self._is_duplicated():
                return self.error
            else:
                # Active method to post in database
                self._save_db()
        except psycopg2.DatabaseError as e:
            # Push error []
            self.error.append(f"Error: {e}")
        finally:
            # Desconnected database but if error exist
            if self._conn:
                self._conn.close()

    # Check if user exist in database
    def _is_duplicated(self):
        # query to check in database.
        query = f"SELECT * FROM {self._BUYERUSERTABLE} WHERE email='{self._email}' " \
                f"AND username='{self._username}'"
        try:
            # Execute check
            self._cur.execute(query)
            # All lines recovery to query
            self._rows = self._cur.fetchone()
            # None = Not exist user in database
            if None is self._rows:
                return False
            else:
                # Push error and return True.
                self.error.append(f"Error: Email or username already exist")
                return True
        # Error conection in database check
        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")

    # Chek users in database
    def _check_db(self):
        # Query to check
        query = f"SELECT * FROM {self._BUYERUSERTABLE}"
        try:
            # Execute query and chow all lines to print in _rows
            self._cur.execute(query)
            self._rows = self._cur.fetchall()
            return self._rows
        except psycopg2.DatabaseError as e:
            # Push errors
            self.error.append(f"Error: {e}")

    # Cheking user existent the moment.
    def print_info(self):
        return f"{self._username}, {self._email}, {self._password}, {self._date}"

    def request_login(self, email, password):
        if email is not None and password is not None:
            self._email = email
            self._password = password
            # If I remove this it doesn't work, it's like the "coco" of doom XD
            print(self._password, self.email)
            # Login user
            self._login()
            return self.error
        else:
            # return error and push.
            self.error.append(f"Error: El email o el password estan vacios")
            return self.error

    # Login user
    def _login(self):
        # Query check user exist in database
        query = f"SELECT * FROM {self._BUYERUSERTABLE} WHERE email='{self._email}' AND password='{self._password}'"
        try:
            # Execute query and check lines recovery
            self._cur.execute(query)
            self._rows = self._cur.fetchone()

            # None => User exist
            if None is not self._rows:
                # Insert cookie to chrome
                cookie = http.cookies.SimpleCookie()
                cookie['email'] = self._email
                cookie['email']["path"] = '/login_user_buyer/'
                response = HttpResponse("Login user success")
                response.set_cookie(
                    key='company_name', value=self._email, path="/login_user_buyer/")
                # Close database
                self._conn.close()
            else:
                # Error print user
                self.error.append(
                    f"Error: el password o el email son incorrectos")
        # Error database user.
        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")


class Maker(models.Model):
    """
        Maker administrative class.
        @params: company_name, password, email => basically config to database.
        methods to administrative user:
            set user in database
            check user in database
            push user in database
    """
    _id = None
    _company_name = models.CharField(max_length=30, unique=True, validators=[
                                     ASCIIUsernameValidator()])
    _password = models.CharField(max_length=30, validators=[
                                 UnicodeUsernameValidator()])
    _email = models.EmailField(unique=True)
    _date = None

    # Connection database and check rows cursor recovery
    _connection = None
    _cur = None
    _rows = None

    # CONST
    _MAKERTABLE = "maker"
    _MAKERUSERTABLE = "maker_user"

    error = []

    # Initialize primary info requery.
    def __init__(self, company_name=None, password=None, email=None):
        self._company_name = company_name
        self._password = password
        self._email = email
        self._date = date.today()

        # Database pulse
        self._conn = psycopg2.connect(
            database="babali",
            user="hernani",
            password="03031516h",
            host="localhost",
            port="5432"
        )
        self._cur = self._conn.cursor()

    # Save company in database
    def _save_db(self):
        # query to execute
        query = f"""
        INSERT INTO {self._MAKERUSERTABLE}(company_name, password, email, date)
        VALUES ('{self._company_name}', '{self._password}', '{self._email}', '{self._date}')
        """
        try:
            # Query execute and send the database
            self._cur.execute(query)
            self._conn.commit()
        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")

    # Check info
    def request_save(self):
        try:
            # Duplicated company check
            if self._is_duplicated():
                return self.error
            else:
                # Save company in database
                self._save_db()
        # Check errors.
        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")
        finally:
            # Close connection database
            if self._conn:
                self._conn.close()

    # Check if exist company in database.
    def _is_duplicated(self):
        query = f"SELECT * FROM {self._MAKERUSERTABLE} WHERE email='{self._email}' " \
                f"AND company_name='{self._company_name}'"
        try:
            # Execute query and check rows walk the query
            self._cur.execute(query)
            self._rows = self._cur.fetchone()
            # None = not exist company in database
            if None is self._rows:
                return False
            else:
                # exist company, push error.
                self.error.append(
                    f"Error: El email o la compania ya esta registrada")
                return True
        # Erorr check
        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")

    # PRint info database
    def _check_db(self):
        query = f"SELECT * FROM {self._MAKERUSERTABLE}"
        try:
            self._cur.execute(query)
            self._rows = self._cur.fetchall()
            # Rows/Table return.
            return self._rows
        except psycopg2.DatabaseError as e:
            self.error.append(f"eError: {e}")

    # Print info in service.
    def print_info(self):
        return f"{self._company_name}, {self._email}, {self._password}, {self._date}"

    # Send login validate @params and check errors.
    def request_login(self, company_name, password):
        if company_name is not None and password is not None:
            self._company_name = company_name
            self._password = password
            # Login method execute
            self._login()
            return self.error
        else:
            # Return error
            self.error.append(
                f"Error: El nombre de la compania o la contrasena estan vacios")
            return self.error

    # Login user
    def _login(self):
        # query to check exist company in database
        query = f"SELECT * FROM {self._MAKERUSERTABLE} WHERE company_name='{self._company_name}' " \
                f"AND password='{self._password}'"
        try:
            # Execute query and check rows walk in query
            self._cur.execute(query)
            self._rows = self._cur.fetchone()
            # not None => company and password they correct.
            if None is not self._rows:
                # Send cookie to info relevant
                cookie = http.cookies.SimpleCookie()
                cookie['company_name'] = self._company_name
                cookie['company_name']["path"] = '/'

                response = HttpResponse("Login company success")
                response.set_cookie(key='company_name',
                                    value=self._company_name, path="/")
                # Close connection database
                self._conn.close()
            else:
                self.error.append(
                    f"Error: La contrasena o el nombre de la compania son incorrectos")

        # Error in database
        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")

# Form value


class ManagerCustomUserMaker(BaseUserManager):
    # Create user validate fields
    def create_user(self, company_name, email, password=None):
        if not email:
            raise ValueError("Correo electronico vacio")

        # Initialize new model
        user = self.model(
            email=self.normalize_email(email),
            company_name=company_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


# Form push
class CustomUserMaker(AbstractUser):
    # Create fields for that form
    company_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=30)

    # Requeriments to django
    active = models.BooleanField(('active'), default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = ManagerCustomUserMaker()

    USERNAME_FIELD = 'company_name'
    REQUIRED_FIELDS = ["company_name"]

    groups = models.ManyToManyField(
        Group, related_name="customusermaker_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="customusermaker_set", blank=True)

    class Meta:
        verbose_name = ("Custom_user_maker")
        verbose_name_plural = ("Custom_user_makers")

    @property
    def is_staff(self):
        """El usuario cuenta con los permisos?"""
        return self.staff

    @property
    def is_admin(self):
        """El usuario es admin?"""
        return self.admin

    @property
    def is_active(self):
        """El usuario esta activo?"""
        return self.active
