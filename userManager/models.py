from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager, Group, Permission
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from http.server import BaseHTTPRequestHandler, HTTPServer
from django.http import HttpResponse
from datetime import date
import psycopg2
import json
import http.cookies


class Buyer(models.Model):
    """
        New Buyer in system
        initialize db and dates requires for the table
    """
    _id = None
    _username = models.CharField(max_length=30, unique=True, validators=[ASCIIUsernameValidator()])
    _password = models.CharField(max_length=30, validators=[UnicodeUsernameValidator()])
    _email = models.EmailField(unique=True)
    _first_name = models.CharField(max_length=30)
    _last_name = models.CharField(max_length=30)
    _date = None
    _connection = None
    _cur = None
    _rows = None

    _BUYERTABLE = "Buyer"
    _BUYERUSERTABLE = "buyer_user"

    error = []

    def __init__(self, username=None, password=None, email=None, first_name=None, last_name=None):
        self._username = username
        self._password = password
        self._email = email
        self._first_name = first_name
        self._last_name = last_name
        self._date = date.today()
        self._conn = psycopg2.connect(
            database="babali",
            user="hernani",
            password="03031516h",
            host="localhost",
            port="5432"
        )
        self._cur = self._conn.cursor()

    def _save_db(self):
        query = f"""
        INSERT INTO {self._BUYERUSERTABLE}(username, password, email, first_name, last_name, date_requested)
        VALUES ('{self._username}', '{self._password}', '{self._email}', '{self._first_name}', '{self._last_name}',
        '{self._date}')
        """
        try:
            self._cur.execute(query)
            self._conn.commit()
        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")

    def request_save(self):
        try:
            if self._is_duplicated():
                return self.error
            else:
                self._save_db()
        except psycopg2.DatabaseError as e:
            print(f"Error: {e}")
            self.error.append(f"Error: {e}")
        finally:
            if self._conn:
                self._conn.close()

    def _is_duplicated(self):
        query = f"SELECT * FROM {self._BUYERUSERTABLE} WHERE email='{self._email}' " \
                f"AND username='{self._username}'"
        try:
            self._cur.execute(query)
            self._rows = self._cur.fetchone()
            if None is self._rows:
                return False
            else:
                self.error.append(f"Error: Email or username already exist")
                return True
        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")

    def _check_db(self):
        query = f"SELECT * FROM {self._BUYERUSERTABLE}"
        try:
            self._cur.execute(query)
            self._rows = self._cur.fetchall()
            return self._rows
        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")

    def print_info(self):
        return f"{self._username}, {self._email}, {self._password}, {self._date}"

    def request_login(self, email, password):
        if email is not None and password is not None:
            self._email = email
            self._password = password
            # Si le quito esto no funciono, es como el coco de doom XD

            self._login()
            return self.error
        else:
            self.error.append(f"Error: El email o el password estan vacios")
            return self.error

    def _login(self):
        query = f"SELECT * FROM {self._BUYERUSERTABLE} WHERE email='{self._email}' AND password='{self._password}'"
        try:
            self._cur.execute(query)
            self._rows = self._cur.fetchone()
            if None is not self._rows:
                cookie = http.cookies.SimpleCookie()
                cookie['email'] = self._email
                cookie['email']["path"] = '/login_user_buyer/'
                response = HttpResponse("Login user success")
                response.set_cookie(key='company_name', value=self._email, path="/login_user_buyer/")
                self._conn.close()
            else:
                self.error.append(f"Error: el password o el email son incorrectos")

        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")


class Maker(models.Model):
    """
        New Buyer in system
        initialize db and dates requires for the table
    """
    _id = None
    _company_name = models.CharField(max_length=30, unique=True, validators=[ASCIIUsernameValidator()])
    _password = models.CharField(max_length=30, validators=[UnicodeUsernameValidator()])
    _email = models.EmailField(unique=True)
    _date = None
    _connection = None
    _cur = None
    _rows = None

    _MAKERTABLE = "maker"
    _MAKERUSERTABLE = "maker_user"

    error = []

    def __init__(self, company_name=None, password=None, email=None):
        self._company_name = company_name
        self._password = password
        self._email = email
        self._date = date.today()

        self._conn = psycopg2.connect(
            database="babali",
            user="hernani",
            password="03031516h",
            host="localhost",
            port="5432"
        )
        self._cur = self._conn.cursor()

    def _save_db(self):
        query = f"""
        INSERT INTO {self._MAKERUSERTABLE}(company_name, password, email, date)
        VALUES ('{self._company_name}', '{self._password}', '{self._email}', '{self._date}')
        """
        try:
            self._cur.execute(query)
            self._conn.commit()
        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")

    def request_save(self):
        try:
            if self._is_duplicated():
                return self.error
            else:
                self._save_db()
        except psycopg2.DatabaseError as e:
            print(f"Error: {e}")
            self.error.append(f"Error: {e}")
        finally:
            if self._conn:
                self._conn.close()

    def _is_duplicated(self):
        query = f"SELECT * FROM {self._MAKERUSERTABLE} WHERE email='{self._email}' " \
                f"AND company_name='{self._company_name}'"
        try:
            self._cur.execute(query)
            self._rows = self._cur.fetchone()
            if None is self._rows:
                return False
            else:
                self.error.append(f"Error: Email or company already exist")
                return True
        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")

    def _check_db(self):
        query = f"SELECT * FROM {self._MAKERUSERTABLE}"
        try:
            self._cur.execute(query)
            self._rows = self._cur.fetchall()
            return self._rows
        except psycopg2.DatabaseError as e:
            self.error.append(f"eError: {e}")

    def print_info(self):
        return f"{self._company_name}, {self._email}, {self._password}, {self._date}"

    def request_login(self, company_name, password):
        if company_name is not None and password is not None:
            self._company_name = company_name
            self._password = password
            self._login()
            return self.error
        else:
            self.error.append(f"Error: El company name o el password estan vacios")
            return self.error

    def _login(self):
        query = f"SELECT * FROM {self._MAKERUSERTABLE} WHERE company_name='{self._company_name}' " \
                f"AND password='{self._password}'"
        try:
            self._cur.execute(query)
            self._rows = self._cur.fetchone()
            if None is not self._rows:
                cookie = http.cookies.SimpleCookie()
                cookie['company_name'] = self._company_name
                cookie['company_name']["path"] = '/'

                response = HttpResponse("Login company success")
                response.set_cookie(key='company_name', value=self._company_name, path="/")
                self._conn.close()
            else:
                self.error.append(f"Error: el password o el company name son incorrectos")

        except psycopg2.DatabaseError as e:
            self.error.append(f"Error: {e}")


class ManagerCustomUserMaker(BaseUserManager):
    def create_user(self, company_name, email, password=None):
        if not email:
            raise ValueError("Correo electronico vacio")

        user = self.model(
            email=self.normalize_email(email),
            company_name=company_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUserMaker(AbstractUser):
    company_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=30)

    active = models.BooleanField(('active'), default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = ManagerCustomUserMaker()

    USERNAME_FIELD = 'company_name'
    REQUIRED_FIELDS = ["company_name"]

    groups = models.ManyToManyField(Group, related_name="customusermaker_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customusermaker_set", blank=True)

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


