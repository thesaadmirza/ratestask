# ratestask

Implementation part of https://github.com/xeneta/ratestask




# Deployment 

1. Env Update From /config/settings
Create .env file by copying .env.example. Update Db Credentials if different 
   



**`Without Docker Configurations`**

**2.Installing Requirements**
`pip install -r requirements.txt`

**3. Run Migrations**
`python3 manage.py migrate`
   
**4. Dump Rates into Postgres**
`psql ratestask < rates.sql`
   
**5. Run the Server**
`python3 manage.py runserver`


**`With Docker Configurations`**

2. Run `docker-compose up` and you are ready to go
check the browser on `127.0.0.1:8000`
