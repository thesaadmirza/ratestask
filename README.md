# ratestask

Implementation part of https://github.com/xeneta/ratestask




# Deployment 

1. Database Configurations
Change DB Connection Credentials in config/settins.py
   `DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ratestask',
        'USER': 'saadmirza',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}`

**2.Installing Requirements**
`pip install -r requirements.txt`

**3. Run Migrations**
`python3 manage.py migrate`
   
**4. Dump Rates into Postgres**
`psql ratestask < rates.sql`
   
**5. Run the Server**
`python3 manage.py runserver`