# [Divar](https://divar.ir/)

### What is this project:

This project is the MVP version of [divar](https://divar.ir/) which developing with Django framework.

---

### Project requirements:

- [x] users can register and login with phone number.
- [x] each user can share his advertisements.
- [x] each user can watch other user's advertisements.
- [x] advertisements should have a category.
- [x] each category should have its properties.
- [x] in advertisements should show user information which this created it.
- [x] users can search in advertisements with price and instantaneous.
- [x] users can update, delete, promotion his advertisement.

---

### The goal of this project for me:

I just hope this project a good resume and practice for me :smiley: :innocent:

---

## Installation:

### In first step:

```
git clone https://github.com/MrMohammadY/Divar
 ```

### In second step:

you should create the virtualenv and active that and install requirements

```
pip install requirements.txt 
```

**after that we have this tree:**

```
│───accounts
│───advertisement
│───divar
|   |───__init__.py
|   |───asgi.py
|   |───settings.py
|   └───wsgi.py
│───lib
│───promotion
│───promotion
│───templates
│───transaction
│───.gitignore
│───LICENCE
│───manage.py
│───README.md       
└───requirements.txt       
```

### In third step:

you should go to divar directory and create and write these**

```
SECRET_KEY = '<your_secret_key>'
DEBUG = True
ALLOWED_HOSTS = []


NAME = '<your_database_name>'
USER = '<your_username>'
PASS = '<your_password>'
HOST = '127.0.0.1'
PORT = 5432 # postgresql port

```

into **local_settings.py**

### In fourth step:

you should make migrations:

```
python manage.py makemigrations
```

and after that:

```
python manage.py migrate
```

### In last step:

you can run project, I hope you enjoy of this